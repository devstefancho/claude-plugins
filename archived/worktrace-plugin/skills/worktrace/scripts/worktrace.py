#!/usr/bin/env python3
"""
Worktrace - Extract Claude Code work history and generate daily summaries.

This script reads ~/.claude/history.jsonl, extracts today's activities,
groups them by project/ticket, and generates a markdown summary.
"""

import argparse
import json
import os
import re
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional


def get_start_of_day_epoch_ms(date_str: Optional[str] = None, tz_name: Optional[str] = None) -> int:
    """Get epoch timestamp in milliseconds for start of day (00:00:00).

    Args:
        date_str: Date in YYYY-MM-DD format. Defaults to today.
        tz_name: Timezone name (e.g., 'Asia/Seoul'). Defaults to system timezone.

    Returns:
        Epoch timestamp in milliseconds for 00:00:00 of the given date.
    """
    try:
        import zoneinfo
        tz = zoneinfo.ZoneInfo(tz_name) if tz_name else None
    except ImportError:
        tz = None

    if date_str:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
    else:
        dt = datetime.now(tz) if tz else datetime.now()

    start_of_day = dt.replace(hour=0, minute=0, second=0, microsecond=0)

    if tz:
        start_of_day = start_of_day.replace(tzinfo=tz)
        return int(start_of_day.timestamp() * 1000)

    return int(start_of_day.timestamp() * 1000)


def load_history(history_file: Path) -> list[dict]:
    """Load history entries from JSONL file.

    Args:
        history_file: Path to history.jsonl file.

    Returns:
        List of history entry dictionaries.
    """
    entries = []
    if not history_file.exists():
        return entries

    with open(history_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    entries.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    return entries


def filter_entries_by_date(entries: list[dict], start_epoch_ms: int) -> list[dict]:
    """Filter history entries to only include those from the given start time.

    Args:
        entries: List of history entries.
        start_epoch_ms: Start epoch timestamp in milliseconds.

    Returns:
        Filtered list of entries.
    """
    return [e for e in entries if e.get("timestamp", 0) >= start_epoch_ms]


def extract_ticket(project_path: str, patterns: list[str]) -> Optional[str]:
    """Extract ticket number from project path using given patterns.

    Args:
        project_path: Full project path.
        patterns: List of regex patterns for ticket matching.

    Returns:
        Extracted ticket number or None.
    """
    for pattern in patterns:
        match = re.search(pattern, project_path)
        if match:
            return match.group(0)
    return None


def extract_project_name(project_path: str) -> str:
    """Extract meaningful project name from full path.

    Args:
        project_path: Full project path.

    Returns:
        Extracted project name.
    """
    parts = project_path.rstrip("/").split("/")

    # Look for common project indicators
    for i, part in enumerate(parts):
        if part in ("feat", "feature", "bugfix", "fix", "hotfix", "release"):
            # Return the parent directory name
            if i > 0:
                return parts[i - 1]
        if part == "projects" and i + 1 < len(parts):
            return parts[i + 1]

    # Fallback: return last meaningful directory
    for part in reversed(parts):
        if part and part not in (".", ""):
            return part

    return project_path


def encode_project_path(path: str) -> str:
    """Encode project path to Claude's directory name format.

    Args:
        path: Full project path (e.g., /Users/foo/bar).

    Returns:
        Encoded directory name (e.g., -Users-foo-bar).
    """
    return re.sub(r"[/.]", "-", path)


def find_session_ids(project_path: str, start_epoch_ms: int, end_epoch_ms: int) -> list[str]:
    """Find session IDs for a project within the given time range.

    Args:
        project_path: Full project path.
        start_epoch_ms: Start epoch timestamp in milliseconds.
        end_epoch_ms: End epoch timestamp in milliseconds.

    Returns:
        List of session IDs active during the time range.
    """
    encoded = encode_project_path(project_path)
    sessions_dir = Path.home() / ".claude" / "projects" / encoded

    if not sessions_dir.exists():
        return []

    session_ids = []
    for session_file in sessions_dir.glob("*.jsonl"):
        # Skip non-UUID files (like agent-*.jsonl)
        session_id = session_file.stem
        if not re.match(r"^[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}$", session_id):
            continue

        # Check first few lines for timestamp
        try:
            with open(session_file, "r", encoding="utf-8") as f:
                for i, line in enumerate(f):
                    if i > 5:  # Only check first few lines
                        break
                    try:
                        entry = json.loads(line)
                        ts = entry.get("timestamp")
                        if ts:
                            # Handle ISO format timestamp
                            if isinstance(ts, str):
                                dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
                                ts_ms = int(dt.timestamp() * 1000)
                            else:
                                ts_ms = ts

                            if start_epoch_ms <= ts_ms <= end_epoch_ms:
                                session_ids.append(session_id)
                                break
                    except (json.JSONDecodeError, ValueError):
                        continue
        except (IOError, OSError):
            continue

    return session_ids


def format_time(timestamp_ms: int) -> str:
    """Format timestamp to HH:MM.

    Args:
        timestamp_ms: Timestamp in milliseconds.

    Returns:
        Formatted time string.
    """
    dt = datetime.fromtimestamp(timestamp_ms / 1000)
    return dt.strftime("%H:%M")


def summarize_activity(display: str, max_length: int = 60) -> str:
    """Summarize activity from display text.

    Args:
        display: Raw display text from history.
        max_length: Maximum length for summary.

    Returns:
        Summarized activity string.
    """
    # Clean up the display text
    summary = display.strip()

    # Truncate if too long
    if len(summary) > max_length:
        summary = summary[:max_length - 3] + "..."

    return summary


def group_by_ticket_and_project(
    entries: list[dict],
    ticket_patterns: list[str],
    start_epoch_ms: int = 0,
    end_epoch_ms: int = 0
) -> dict[str, dict]:
    """Group entries by ticket number or project.

    Args:
        entries: List of history entries.
        ticket_patterns: List of regex patterns for ticket matching.
        start_epoch_ms: Start epoch for session lookup.
        end_epoch_ms: End epoch for session lookup.

    Returns:
        Dictionary mapping group keys to group info (entries, directory, session_ids).
    """
    groups = defaultdict(lambda: {"entries": [], "directory": "", "session_ids": set()})

    for entry in entries:
        project = entry.get("project", "")
        ticket = extract_ticket(project, ticket_patterns)
        project_name = extract_project_name(project)

        if ticket:
            key = f"{ticket} ({project_name})"
        else:
            key = f"Other ({project_name})"

        groups[key]["entries"].append(entry)
        groups[key]["directory"] = project

        # Find session IDs for this project
        if start_epoch_ms and end_epoch_ms:
            session_ids = find_session_ids(project, start_epoch_ms, end_epoch_ms)
            groups[key]["session_ids"].update(session_ids)

    # Convert sets to sorted lists
    result = {}
    for key, value in groups.items():
        result[key] = {
            "entries": value["entries"],
            "directory": value["directory"],
            "session_ids": sorted(value["session_ids"])
        }

    return result


def generate_markdown(
    groups: dict[str, dict],
    section_title: str = "## Claude Code Work History"
) -> str:
    """Generate markdown output from grouped entries.

    Args:
        groups: Dictionary of grouped entries with directory and session info.
        section_title: Title for the section.

    Returns:
        Markdown formatted string.
    """
    lines = [section_title, ""]

    # Sort groups: tickets first (alphabetically), then "Other" groups
    sorted_keys = sorted(groups.keys(), key=lambda k: (k.startswith("Other"), k))

    for key in sorted_keys:
        group_info = groups[key]
        entries = group_info.get("entries", [])
        directory = group_info.get("directory", "")
        session_ids = group_info.get("session_ids", [])

        lines.append(f"### {key}")

        # Add directory info
        if directory:
            lines.append(f"- **Directory**: `{directory}`")

        # Add session IDs
        if session_ids:
            if len(session_ids) == 1:
                lines.append(f"- **Session**: `{session_ids[0]}`")
            else:
                sessions_str = ", ".join(f"`{s}`" for s in session_ids[:3])
                if len(session_ids) > 3:
                    sessions_str += f" (+{len(session_ids) - 3} more)"
                lines.append(f"- **Sessions**: {sessions_str}")

        # Deduplicate and summarize activities
        seen = set()
        for entry in entries:
            display = entry.get("display", "")
            summary = summarize_activity(display)

            if summary and summary not in seen:
                seen.add(summary)
                lines.append(f"- {summary}")

        lines.append("")

    return "\n".join(lines)


def load_config(config_path: Optional[Path]) -> dict:
    """Load configuration from JSON file.

    Args:
        config_path: Path to config file.

    Returns:
        Configuration dictionary.
    """
    if config_path and config_path.exists():
        with open(config_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def main():
    parser = argparse.ArgumentParser(
        description="Extract Claude Code work history and generate daily summaries."
    )
    parser.add_argument(
        "--history-file",
        type=Path,
        default=Path.home() / ".claude" / "history.jsonl",
        help="Path to history.jsonl (default: ~/.claude/history.jsonl)"
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        help="Directory to save daily file (if not specified, prints to stdout)"
    )
    parser.add_argument(
        "--ticket-pattern",
        action="append",
        dest="ticket_patterns",
        help="Regex pattern for ticket matching (can be specified multiple times)"
    )
    parser.add_argument(
        "--date",
        type=str,
        help="Target date in YYYY-MM-DD format (default: today)"
    )
    parser.add_argument(
        "--timezone",
        type=str,
        help="Timezone name (e.g., Asia/Seoul)"
    )
    parser.add_argument(
        "--config",
        type=Path,
        help="Path to config JSON file"
    )
    parser.add_argument(
        "--section-title",
        type=str,
        default="## Claude Code Work History",
        help="Section title for the output"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output as JSON instead of markdown"
    )

    args = parser.parse_args()

    # Load config and merge with CLI args
    config = load_config(args.config)

    history_file = args.history_file
    if "history_file" in config:
        history_file = Path(os.path.expanduser(config["history_file"]))

    ticket_patterns = args.ticket_patterns or config.get("ticket_patterns", [r"[A-Z]+-\d+"])
    timezone = args.timezone or config.get("timezone")
    section_title = args.section_title
    if "section_title" in config:
        section_title = config["section_title"]

    # Get start of day epoch
    target_date = args.date
    start_epoch_ms = get_start_of_day_epoch_ms(target_date, timezone)
    # End of day is start + 24 hours
    end_epoch_ms = start_epoch_ms + (24 * 60 * 60 * 1000)

    # Load and filter history
    entries = load_history(history_file)
    filtered = filter_entries_by_date(entries, start_epoch_ms)

    if not filtered:
        print("No entries found for the specified date.", file=sys.stderr)
        sys.exit(0)

    # Group and generate output
    groups = group_by_ticket_and_project(filtered, ticket_patterns, start_epoch_ms, end_epoch_ms)

    if args.json:
        output = json.dumps({
            "date": target_date or datetime.now().strftime("%Y-%m-%d"),
            "entries_count": len(filtered),
            "groups": {
                k: {
                    "directory": v["directory"],
                    "session_ids": v["session_ids"],
                    "activities": [e.get("display", "") for e in v["entries"]]
                }
                for k, v in groups.items()
            }
        }, indent=2, ensure_ascii=False)
    else:
        output = generate_markdown(groups, section_title)

    # Output
    if args.output_dir:
        date_str = target_date or datetime.now().strftime("%Y-%m-%d")
        output_file = args.output_dir / f"{date_str}.md"

        # If file exists, update only the section
        if output_file.exists():
            with open(output_file, "r", encoding="utf-8") as f:
                content = f.read()

            # Find and replace section
            section_pattern = rf"({re.escape(section_title)})\n[\s\S]*?(?=\n## |\Z)"
            if re.search(section_pattern, content):
                content = re.sub(section_pattern, output.rstrip(), content)
            else:
                # Append section after first heading
                first_heading = re.search(r"^# .+$", content, re.MULTILINE)
                if first_heading:
                    pos = first_heading.end()
                    content = content[:pos] + "\n\n" + output + content[pos:]
                else:
                    content = content + "\n\n" + output

            with open(output_file, "w", encoding="utf-8") as f:
                f.write(content)
        else:
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(output)

        print(f"Updated: {output_file}", file=sys.stderr)
    else:
        print(output)


if __name__ == "__main__":
    main()
