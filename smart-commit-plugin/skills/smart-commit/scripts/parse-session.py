#!/usr/bin/env python3
"""
parse-session.py - Parse Claude Code session JSONL to extract file operations and user messages.

Reads session conversation data from ~/.claude/projects/{encoded-path}/{sessionId}.jsonl
and extracts structured information about file edits, writes, and user intent.

Output: JSON to stdout with session_id, project_path, user_messages, file_ops, snapshots.
Errors: [ERROR] and [HINT] messages to stderr.
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Optional


def encode_project_path(path: str) -> str:
    """Encode project path to Claude's directory name format.

    Reused from worktrace-plugin pattern.
    e.g., /Users/foo/bar → -Users-foo-bar
    """
    return re.sub(r"[/.]", "-", path)


def load_jsonl(filepath: Path) -> list[dict]:
    """Safely load a JSONL file, skipping malformed lines."""
    entries = []
    if not filepath.exists():
        return entries
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    entries.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    return entries


def find_latest_session(project_path: str, history_file: Path) -> Optional[str]:
    """Find the most recent session ID for a project from history.jsonl."""
    entries = load_jsonl(history_file)
    # history.jsonl entries have project paths and session references
    # Filter entries matching our project
    matching = []
    for entry in entries:
        entry_project = entry.get("project", "")
        if entry_project and os.path.normpath(entry_project) == os.path.normpath(project_path):
            matching.append(entry)

    if not matching:
        return None

    # Sort by timestamp descending, return latest session_id
    matching.sort(key=lambda e: e.get("timestamp", 0), reverse=True)
    return matching[0].get("sessionId") or matching[0].get("session_id")


def find_session_from_projects_dir(project_path: str) -> Optional[str]:
    """Find latest session by checking the projects directory directly."""
    encoded = encode_project_path(project_path)
    sessions_dir = Path.home() / ".claude" / "projects" / encoded

    if not sessions_dir.exists():
        return None

    # Find most recently modified session JSONL
    session_files = []
    for f in sessions_dir.glob("*.jsonl"):
        # Only UUID-named session files
        if re.match(r"^[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}$", f.stem):
            session_files.append(f)

    if not session_files:
        return None

    # Sort by modification time, latest first
    session_files.sort(key=lambda f: f.stat().st_mtime, reverse=True)
    return session_files[0].stem


def parse_timestamp(ts) -> Optional[int]:
    """Parse timestamp to epoch milliseconds. Handles both int and ISO string."""
    if isinstance(ts, (int, float)):
        return int(ts)
    if isinstance(ts, str):
        try:
            from datetime import datetime
            dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
            return int(dt.timestamp() * 1000)
        except (ValueError, TypeError):
            return None
    return None


def extract_tool_calls(message: dict) -> list[dict]:
    """Extract tool use blocks from an assistant message."""
    tools = []
    content = message.get("content", [])
    if isinstance(content, str):
        return tools
    for block in content:
        if isinstance(block, dict) and block.get("type") == "tool_use":
            tools.append(block)
    return tools


def extract_file_ops_from_tool(tool: dict, project_path: str) -> Optional[dict]:
    """Extract file operation info from a tool_use block."""
    name = tool.get("name", "")
    inp = tool.get("input", {})

    if name not in ("Edit", "Write", "NotebookEdit"):
        return None

    file_path = inp.get("file_path", "")
    if not file_path:
        return None

    # Filter out files outside the project
    norm_project = os.path.normpath(project_path)
    norm_file = os.path.normpath(file_path)
    if not norm_file.startswith(norm_project):
        return None

    # Determine change type
    if name == "Write":
        change = "write"
    elif name == "Edit":
        change = "edit"
    elif name == "NotebookEdit":
        change = "notebook_edit"
    else:
        change = "unknown"

    # Make path relative to project
    rel_path = os.path.relpath(norm_file, norm_project)

    return {
        "path": rel_path,
        "absolute_path": file_path,
        "tool": name,
        "change": change,
    }


def extract_user_text(message: dict) -> Optional[str]:
    """Extract text content from a user message."""
    content = message.get("content", "")
    if isinstance(content, str):
        return content.strip() if content.strip() else None
    if isinstance(content, list):
        texts = []
        for block in content:
            if isinstance(block, dict) and block.get("type") == "text":
                texts.append(block.get("text", ""))
            elif isinstance(block, str):
                texts.append(block)
        combined = " ".join(texts).strip()
        return combined if combined else None
    return None


def parse_session(session_file: Path, project_path: str, verbose: bool = False) -> dict:
    """Parse a session JSONL file and extract structured data."""
    entries = load_jsonl(session_file)

    user_messages = []
    file_ops = []
    snapshots = []
    current_timestamp = None
    user_msg_index = 0

    for entry in entries:
        entry_type = entry.get("type")
        ts = parse_timestamp(entry.get("timestamp"))

        if ts:
            current_timestamp = ts

        # User messages
        if entry_type == "human" or entry.get("role") == "human":
            text = extract_user_text(entry)
            if text:
                # Skip system-generated messages
                if text.startswith("<system-reminder>") or text.startswith("{\"type\":"):
                    continue
                user_messages.append({
                    "index": user_msg_index,
                    "timestamp": current_timestamp,
                    "text": text[:500],  # Truncate long messages
                })
                user_msg_index += 1
                if verbose:
                    preview = text[:80].replace("\n", " ")
                    print(f"[VERBOSE] User message {user_msg_index}: {preview}", file=sys.stderr)

        # Assistant messages with tool calls
        elif entry_type == "assistant" or entry.get("role") == "assistant":
            tools = extract_tool_calls(entry)
            for tool in tools:
                op = extract_file_ops_from_tool(tool, project_path)
                if op:
                    op["timestamp"] = current_timestamp
                    op["user_msg_index"] = max(0, user_msg_index - 1)
                    file_ops.append(op)
                    if verbose:
                        print(f"[VERBOSE] File op: {op['change']} {op['path']}", file=sys.stderr)

        # File history snapshots
        elif entry_type == "file-history-snapshot":
            snapshot_data = entry.get("data", {})
            if snapshot_data:
                snapshots.append({
                    "timestamp": current_timestamp,
                    "files": snapshot_data,
                })

    return {
        "session_id": session_file.stem,
        "project_path": project_path,
        "user_messages": user_messages,
        "file_ops": file_ops,
        "snapshots": snapshots,
    }


def main():
    parser = argparse.ArgumentParser(
        description="Parse Claude Code session JSONL to extract file operations and user messages."
    )
    parser.add_argument(
        "--project",
        type=str,
        required=False,
        help="Project directory path (auto-detects latest session)"
    )
    parser.add_argument(
        "--session",
        type=str,
        required=False,
        help="Specific session ID to parse"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print detailed parsing log to stderr"
    )

    args = parser.parse_args()

    # Determine project path
    project_path = args.project or os.getcwd()
    project_path = os.path.normpath(os.path.expanduser(project_path))

    if args.verbose:
        print(f"[VERBOSE] Project path: {project_path}", file=sys.stderr)

    # Determine session ID
    session_id = args.session
    if not session_id:
        history_file = Path.home() / ".claude" / "history.jsonl"
        session_id = find_latest_session(project_path, history_file)

    if not session_id:
        # Fallback: check projects directory directly
        session_id = find_session_from_projects_dir(project_path)

    if not session_id:
        print("[ERROR] No session found for this project.", file=sys.stderr)
        print("[HINT] Use --session <id> to specify a session ID manually.", file=sys.stderr)
        print("[HINT] Check ~/.claude/history.jsonl for available sessions.", file=sys.stderr)
        sys.exit(1)

    if args.verbose:
        print(f"[VERBOSE] Session ID: {session_id}", file=sys.stderr)

    # Find session JSONL file
    encoded = encode_project_path(project_path)
    session_file = Path.home() / ".claude" / "projects" / encoded / f"{session_id}.jsonl"

    if not session_file.exists():
        print(f"[ERROR] Session file not found: {session_file}", file=sys.stderr)
        print("[HINT] The session may have been cleared or the path encoding may differ.", file=sys.stderr)
        print(f"[HINT] Expected encoded path: {encoded}", file=sys.stderr)
        sys.exit(1)

    if args.verbose:
        print(f"[VERBOSE] Session file: {session_file}", file=sys.stderr)

    # Parse the session
    result = parse_session(session_file, project_path, verbose=args.verbose)

    if not result["file_ops"]:
        print("[ERROR] No file operations found in session.", file=sys.stderr)
        print("[HINT] This session may not contain any Edit/Write tool calls.", file=sys.stderr)
        sys.exit(1)

    # Output JSON
    print(json.dumps(result, indent=2, ensure_ascii=False))

    if args.verbose:
        print(f"[VERBOSE] Found {len(result['user_messages'])} user messages", file=sys.stderr)
        print(f"[VERBOSE] Found {len(result['file_ops'])} file operations", file=sys.stderr)
        print(f"[VERBOSE] Found {len(result['snapshots'])} snapshots", file=sys.stderr)


if __name__ == "__main__":
    main()
