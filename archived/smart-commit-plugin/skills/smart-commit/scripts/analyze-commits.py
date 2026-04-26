#!/usr/bin/env python3
"""
analyze-commits.py - Analyze parsed session data to produce logical commit groups.

Takes output from parse-session.py and groups file operations into logical commits
based on user intent boundaries, timestamp gaps, and file relationships.
Automatically merges groups that share overlapping files.

Output: JSON to stdout with commit_groups, merged_groups, and summary.
"""

import argparse
import json
import re
import sys
from collections import defaultdict
from typing import Optional


# Conventional commit type keywords
TYPE_KEYWORDS = {
    "feat": [
        "add", "create", "implement", "new", "feature", "introduce",
        "추가", "생성", "구현", "새로", "기능",
    ],
    "fix": [
        "fix", "bug", "error", "resolve", "patch", "correct",
        "수정", "버그", "에러", "고치", "오류",
    ],
    "refactor": [
        "refactor", "restructure", "reorganize", "clean", "simplify", "move",
        "리팩토", "정리", "개선", "구조",
    ],
    "style": [
        "style", "format", "lint", "whitespace", "indent",
        "스타일", "포맷", "정렬",
    ],
    "docs": [
        "doc", "readme", "comment", "description",
        "문서", "주석", "설명",
    ],
    "test": [
        "test", "spec", "coverage", "assert",
        "테스트", "검증",
    ],
    "chore": [
        "config", "build", "ci", "dependency", "setup", "update",
        "설정", "빌드", "의존",
    ],
}


def detect_commit_type(user_context: str, files: list[dict]) -> str:
    """Detect conventional commit type from user context and file paths."""
    context_lower = user_context.lower()

    # Check user context against keywords
    for commit_type, keywords in TYPE_KEYWORDS.items():
        for kw in keywords:
            if kw in context_lower:
                return commit_type

    # Infer from file paths
    file_paths = [f["path"] for f in files]
    path_str = " ".join(file_paths).lower()

    if any(p for p in file_paths if "test" in p.lower() or "spec" in p.lower()):
        return "test"
    if any(p for p in file_paths if p.lower().endswith((".md", ".txt", ".rst"))):
        return "docs"
    if any(p for p in file_paths if "config" in p.lower() or p.lower().startswith(".")):
        return "chore"

    # Default
    return "feat"


def generate_commit_message(user_context: str, files: list[dict], commit_type: str) -> str:
    """Generate a concise commit message from user context."""
    # Clean up user context for message
    msg = user_context.strip()

    # Remove common prefixes
    for prefix in ["해줘", "해주세요", "please", "can you", "could you"]:
        msg = re.sub(rf"\s*{prefix}\s*$", "", msg, flags=re.IGNORECASE)

    # Truncate if too long
    if len(msg) > 72:
        msg = msg[:69] + "..."

    # If message is empty or too short, generate from files
    if len(msg) < 5:
        if len(files) == 1:
            msg = f"update {files[0]['path']}"
        else:
            # Find common directory
            dirs = set(f["path"].rsplit("/", 1)[0] if "/" in f["path"] else "." for f in files)
            if len(dirs) == 1:
                msg = f"update files in {dirs.pop()}"
            else:
                msg = f"update {len(files)} files"

    return msg


def map_ops_to_user_turns(file_ops: list[dict], user_messages: list[dict]) -> list[dict]:
    """Map each file operation to the user message turn that triggered it."""
    if not user_messages:
        # No user messages, treat all ops as one turn
        for op in file_ops:
            op["turn_index"] = 0
            op["user_context"] = ""
        return file_ops

    for op in file_ops:
        op_msg_idx = op.get("user_msg_index", 0)
        # Find the closest user message at or before this index
        matched = None
        for msg in user_messages:
            if msg["index"] <= op_msg_idx:
                matched = msg
            else:
                break

        if matched:
            op["turn_index"] = matched["index"]
            op["user_context"] = matched.get("text", "")
        else:
            op["turn_index"] = 0
            op["user_context"] = user_messages[0].get("text", "") if user_messages else ""

    return file_ops


def detect_intent_boundaries(user_messages: list[dict]) -> list[int]:
    """Detect user intent change boundaries from message sequence.

    Returns list of user message indices where intent changes.
    """
    if len(user_messages) <= 1:
        return []

    boundaries = []
    for i in range(1, len(user_messages)):
        prev = user_messages[i - 1].get("text", "").lower()
        curr = user_messages[i].get("text", "").lower()

        # Explicit intent change indicators
        intent_change_markers = [
            "그리고", "다음으로", "이제", "다른",
            "now", "next", "also", "another", "then",
            "and then", "after that",
        ]
        has_marker = any(marker in curr for marker in intent_change_markers)

        # Topic change: check if texts are substantially different
        prev_words = set(prev.split())
        curr_words = set(curr.split())
        if prev_words and curr_words:
            overlap = len(prev_words & curr_words) / min(len(prev_words), len(curr_words))
            topic_change = overlap < 0.3
        else:
            topic_change = True

        # Time gap check
        prev_ts = user_messages[i - 1].get("timestamp")
        curr_ts = user_messages[i].get("timestamp")
        time_gap = False
        if prev_ts and curr_ts:
            gap_minutes = (curr_ts - prev_ts) / (1000 * 60)
            time_gap = gap_minutes > 5  # 5 minute gap suggests new task

        if has_marker or topic_change or time_gap:
            boundaries.append(user_messages[i]["index"])

    return boundaries


def group_ops_by_turn(file_ops: list[dict], boundaries: list[int]) -> list[list[dict]]:
    """Group file operations into commit groups based on turn boundaries."""
    if not file_ops:
        return []

    # Sort ops by timestamp
    sorted_ops = sorted(file_ops, key=lambda o: o.get("timestamp", 0) or 0)

    groups = []
    current_group = []
    current_boundary_idx = 0

    for op in sorted_ops:
        turn_idx = op.get("turn_index", 0)

        # Check if we've crossed a boundary
        while current_boundary_idx < len(boundaries) and turn_idx >= boundaries[current_boundary_idx]:
            if current_group:
                groups.append(current_group)
                current_group = []
            current_boundary_idx += 1

        current_group.append(op)

    if current_group:
        groups.append(current_group)

    return groups


def merge_overlapping_groups(groups: list[list[dict]]) -> tuple[list[list[dict]], list[dict]]:
    """Merge groups that share overlapping files.

    Returns:
        Tuple of (merged_groups, merge_info)
    """
    if len(groups) <= 1:
        return groups, []

    # Build file -> group indices mapping
    file_to_groups = defaultdict(set)
    for i, group in enumerate(groups):
        for op in group:
            file_to_groups[op["path"]].add(i)

    # Find groups to merge using union-find
    parent = list(range(len(groups)))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[rb] = ra

    merge_info = []
    for filepath, group_indices in file_to_groups.items():
        indices = sorted(group_indices)
        if len(indices) > 1:
            for j in range(1, len(indices)):
                union(indices[0], indices[j])
            merge_info.append({
                "original": [i + 1 for i in indices],  # 1-indexed for display
                "reason": f"shared file: {filepath}",
            })

    # Collect merged groups
    merged = defaultdict(list)
    for i, group in enumerate(groups):
        root = find(i)
        merged[root].extend(group)

    # Deduplicate ops within merged groups (keep latest op per file)
    result = []
    for root in sorted(merged.keys()):
        ops = merged[root]
        seen_files = {}
        for op in ops:
            path = op["path"]
            if path not in seen_files or (op.get("timestamp") or 0) > (seen_files[path].get("timestamp") or 0):
                seen_files[path] = op
        result.append(list(seen_files.values()))

    # Deduplicate merge_info
    seen_merges = set()
    unique_merges = []
    for info in merge_info:
        key = tuple(info["original"])
        if key not in seen_merges:
            seen_merges.add(key)
            unique_merges.append(info)

    return result, unique_merges


def build_commit_groups(groups: list[list[dict]], user_messages: list[dict]) -> list[dict]:
    """Build final commit group structures with messages and types."""
    commit_groups = []

    for i, group_ops in enumerate(groups):
        # Determine user context from the operations
        contexts = []
        for op in group_ops:
            ctx = op.get("user_context", "")
            if ctx and ctx not in contexts:
                contexts.append(ctx)

        user_context = contexts[0] if contexts else ""

        # Build file list
        files = []
        seen_paths = set()
        for op in sorted(group_ops, key=lambda o: o["path"]):
            if op["path"] not in seen_paths:
                seen_paths.add(op["path"])
                files.append({
                    "path": op["path"],
                    "change": op.get("change", "edit"),
                })

        # Detect type and generate message
        commit_type = detect_commit_type(user_context, files)
        message = generate_commit_message(user_context, files, commit_type)

        commit_groups.append({
            "index": i + 1,
            "type": commit_type,
            "message": message,
            "files": files,
            "user_context": user_context[:200],  # Truncate for display
        })

    return commit_groups


def main():
    parser = argparse.ArgumentParser(
        description="Analyze parsed session data to produce logical commit groups."
    )
    parser.add_argument(
        "--session-data",
        type=str,
        required=False,
        help="Path to JSON from parse-session.py (reads stdin if not specified)"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print boundary decision reasoning to stderr"
    )

    args = parser.parse_args()

    # Load session data
    if args.session_data:
        try:
            with open(args.session_data, "r", encoding="utf-8") as f:
                session_data = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"[ERROR] Failed to load session data: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        try:
            session_data = json.load(sys.stdin)
        except json.JSONDecodeError as e:
            print(f"[ERROR] Failed to parse stdin as JSON: {e}", file=sys.stderr)
            print("[HINT] Pipe output from parse-session.py or use --session-data <path>", file=sys.stderr)
            sys.exit(1)

    file_ops = session_data.get("file_ops", [])
    user_messages = session_data.get("user_messages", [])

    if not file_ops:
        print("[ERROR] No file operations to analyze.", file=sys.stderr)
        sys.exit(1)

    if args.verbose:
        print(f"[VERBOSE] Analyzing {len(file_ops)} file ops, {len(user_messages)} user messages", file=sys.stderr)

    # Step 1: Map ops to user turns
    file_ops = map_ops_to_user_turns(file_ops, user_messages)

    # Step 2: Detect intent boundaries
    boundaries = detect_intent_boundaries(user_messages)
    if args.verbose:
        print(f"[VERBOSE] Detected {len(boundaries)} intent boundaries at indices: {boundaries}", file=sys.stderr)

    # Step 3: Group by turn boundaries
    groups = group_ops_by_turn(file_ops, boundaries)
    if args.verbose:
        print(f"[VERBOSE] Initial groups: {len(groups)}", file=sys.stderr)
        for i, g in enumerate(groups):
            files = set(op["path"] for op in g)
            print(f"[VERBOSE]   Group {i+1}: {len(g)} ops, files: {files}", file=sys.stderr)

    # Step 4: Merge overlapping groups
    merged_groups, merge_info = merge_overlapping_groups(groups)
    if args.verbose and merge_info:
        print(f"[VERBOSE] Merged {len(merge_info)} overlapping groups", file=sys.stderr)
        for info in merge_info:
            print(f"[VERBOSE]   Merged groups {info['original']}: {info['reason']}", file=sys.stderr)

    # Step 5: Build commit groups
    commit_groups = build_commit_groups(merged_groups, user_messages)

    # Output
    result = {
        "commit_groups": commit_groups,
        "merged_groups": merge_info,
        "summary": {
            "total_groups": len(commit_groups),
            "merged_count": len(merge_info),
            "total_files": sum(len(g["files"]) for g in commit_groups),
        },
    }

    print(json.dumps(result, indent=2, ensure_ascii=False))

    if args.verbose:
        print(f"[VERBOSE] Output: {len(commit_groups)} commit groups, {len(merge_info)} merges", file=sys.stderr)


if __name__ == "__main__":
    main()
