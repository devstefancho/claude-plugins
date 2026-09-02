#!/usr/bin/env bash
# Locate a previous Claude Code or Codex CLI session transcript and print
# metadata + the last N conversation turns. Portable: macOS (BSD) and Linux (GNU).
#
# Usage:
#   resume.sh                      # most recent previous session for this project
#   resume.sh <uuid-or-substring>  # specific session (Claude or Codex)
#   resume.sh -n N                 # last N conversation turns (default 10)
#   resume.sh --all                # include tool-activity lines, not just text turns
#   resume.sh --list [K]           # list recent sessions for this project (default 10)
#   resume.sh --global             # with --list or auto-detect: search all projects
#
# Auto-detect skips sessions modified in the last $RESUME_ACTIVE_SECS (default
# 120) seconds — the newest file is usually the session you are in right now.
# Read-only: never modifies session files.
set -euo pipefail

command -v jq >/dev/null 2>&1 || { echo "error: jq is required" >&2; exit 2; }

SID="" N=10 MODE=resume LISTK=10 ALL=0 GLOBAL=0
while [[ $# -gt 0 ]]; do
  case "$1" in
    -n) [[ ${2:-} =~ ^[0-9]+$ ]] || { echo "error: -n requires a number" >&2; exit 2; }
        N="$2"; shift 2 ;;
    -a|--all) ALL=1; shift ;;
    -l|--list) MODE=list; shift
        [[ ${1:-} =~ ^[0-9]+$ ]] && { LISTK="$1"; shift; } || true ;;
    -g|--global) GLOBAL=1; shift ;;
    -h|--help) awk '/^#!/{next} /^[^#]/{exit} /^#/{print substr($0,3)}' "$0"; exit 0 ;;
    *) SID="$1"; shift ;;
  esac
done

CLAUDE_DIR="$HOME/.claude/projects"
CODEX_DIR="$HOME/.codex/sessions"
NOW="$(date +%s)"
ACTIVE_SECS="${RESUME_ACTIVE_SECS:-120}"

# --- portability helpers (BSD first, GNU fallback) --------------------------
mtime_epoch() { stat -f '%m' "$1" 2>/dev/null || stat -c '%Y' "$1" 2>/dev/null || echo 0; }
epoch_human() { date -r "$1" '+%Y-%m-%d %H:%M' 2>/dev/null || date -d "@$1" '+%Y-%m-%d %H:%M' 2>/dev/null || echo '?'; }
is_active()   { local e; e="$(mtime_epoch "$1")"; (( NOW - e < ACTIVE_SECS )); }

# Project dir for the current repo/cwd ('/' and '.' both encode to '-').
proj_root="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
enc="$(printf '%s' "$proj_root" | sed 's![/.]!-!g')"
PROJ_DIR="$CLAUDE_DIR/$enc"

# --- metadata helpers --------------------------------------------------------
claude_title() { # ai-title, else summary, else last-prompt snippet
  local f="$1" t=""
  t="$(grep '"type":"ai-title"' "$f" 2>/dev/null | tail -1 | jq -r '.aiTitle // ""' 2>/dev/null)" || true
  [[ -z "$t" ]] && t="$(grep -m1 '"type":"summary"' "$f" 2>/dev/null | jq -r '.summary // ""' 2>/dev/null)" || true
  [[ -z "$t" ]] && t="$(grep '"type":"last-prompt"' "$f" 2>/dev/null | tail -1 | jq -r '(.lastPrompt // "") | .[0:80]' 2>/dev/null)" || true
  printf '%s' "$t"
}

# --- list mode ---------------------------------------------------------------
if [[ "$MODE" == "list" ]]; then
  if [[ "$GLOBAL" == 1 ]]; then
    echo "Recent Claude Code sessions (all projects):"
    files="$(ls -t "$CLAUDE_DIR"/*/*.jsonl 2>/dev/null | head -n "$LISTK")" || true
  else
    echo "Recent Claude Code sessions for $proj_root:"
    files="$(ls -t "$PROJ_DIR"/*.jsonl 2>/dev/null | head -n "$LISTK")" || true
  fi
  if [[ -z "$files" ]]; then
    echo "  (none found — try --global)"
  else
    while IFS= read -r f; do
      e="$(mtime_epoch "$f")"; mark=""; is_active "$f" && mark=" *ACTIVE*"
      t="$(claude_title "$f" | head -c 100)"; [[ -z "$t" ]] && t="(untitled)"
      printf '  %s  %s%s\n      %s\n' "$(epoch_human "$e")" "$(basename "$f" .jsonl)" "$mark" "$t"
    done <<<"$files"
  fi
  if [[ -d "$CODEX_DIR" ]]; then
    cfiles="$(find "$CODEX_DIR" -name 'rollout-*.jsonl' 2>/dev/null)" || true
    if [[ -n "$cfiles" ]]; then
      recent_codex="$(printf '%s\n' "$cfiles" | tr '\n' '\0' | xargs -0 ls -t 2>/dev/null | head -3)" || true
      echo "Recent Codex sessions (global):"
      while IFS= read -r f; do
        [[ -z "$f" ]] && continue
        e="$(mtime_epoch "$f")"; mark=""; is_active "$f" && mark=" *ACTIVE*"
        cwd="$(head -1 "$f" | jq -r '.cwd // .payload.cwd // ""' 2>/dev/null)" || true
        printf '  %s  %s%s  cwd=%s\n' "$(epoch_human "$e")" "$(basename "$f")" "$mark" "$cwd"
      done <<<"$recent_codex"
    fi
  fi
  echo
  echo "resume: resume.sh <uuid> [-n N]   (*ACTIVE* = likely a live session)"
  exit 0
fi

# --- discover the target transcript ------------------------------------------
JSONL=""
skipped_active=0
if [[ -n "$SID" ]]; then
  CANDIDATES=()
  while IFS= read -r f; do
    [[ -n "$f" ]] && CANDIDATES+=("$f")
  done < <(find "$CLAUDE_DIR" "$CODEX_DIR" -name "*${SID}*.jsonl" 2>/dev/null)
  if [[ ${#CANDIDATES[@]} -eq 0 ]]; then
    echo "no session found for '${SID}' (searched $CLAUDE_DIR and $CODEX_DIR)"
    exit 1
  elif [[ ${#CANDIDATES[@]} -gt 1 ]]; then
    echo "multiple sessions match '${SID}' — re-run with a longer UUID:"
    for f in "${CANDIDATES[@]}"; do
      echo "  $(epoch_human "$(mtime_epoch "$f")")  $f"
    done
    exit 1
  fi
  JSONL="${CANDIDATES[0]}"
else
  pick_latest_nonactive() { # newline-separated candidates on stdin, newest first
    local f
    while IFS= read -r f; do
      [[ -z "$f" ]] && continue
      is_active "$f" && continue
      printf '%s' "$f"; return 0
    done
    return 0
  }
  claude_latest=""
  if [[ -d "$PROJ_DIR" ]]; then
    claude_latest="$(ls -t "$PROJ_DIR"/*.jsonl 2>/dev/null | pick_latest_nonactive)" || true
    newest_any="$(ls -t "$PROJ_DIR"/*.jsonl 2>/dev/null | head -1)" || true
    [[ -n "$newest_any" && "$newest_any" != "$claude_latest" ]] && is_active "$newest_any" && skipped_active=1 || true
  fi
  if [[ -z "$claude_latest" && "$GLOBAL" == 1 ]]; then
    claude_latest="$(ls -t "$CLAUDE_DIR"/*/*.jsonl 2>/dev/null | pick_latest_nonactive)" || true
  fi
  codex_latest=""
  if [[ -d "$CODEX_DIR" ]]; then
    cfiles="$(find "$CODEX_DIR" -name 'rollout-*.jsonl' 2>/dev/null)" || true
    [[ -n "$cfiles" ]] && codex_latest="$(printf '%s\n' "$cfiles" | tr '\n' '\0' | xargs -0 ls -t 2>/dev/null | pick_latest_nonactive)" || true
  fi
  # newest of the two
  if [[ -n "$claude_latest" && -n "$codex_latest" ]]; then
    if (( $(mtime_epoch "$claude_latest") >= $(mtime_epoch "$codex_latest") )); then
      JSONL="$claude_latest"
    else
      JSONL="$codex_latest"
    fi
  else
    JSONL="${claude_latest:-$codex_latest}"
  fi
  if [[ -z "$JSONL" ]]; then
    echo "no previous session found for $proj_root"
    (( skipped_active > 0 )) && echo "  ($skipped_active active session(s) skipped — pass a UUID to read a live session)"
    echo "  try: resume.sh --list  or  resume.sh --global"
    exit 1
  fi
fi

case "$JSONL" in
  *"/.claude/projects/"*) TOOL="claude" ;;
  *"/.codex/sessions/"*)  TOOL="codex" ;;
  *)                      TOOL="unknown" ;;
esac

# --- header -------------------------------------------------------------------
e="$(mtime_epoch "$JSONL")"
if [[ "$TOOL" == "claude" ]]; then
  session_id="$(basename "$JSONL" .jsonl)"
  hdr="$(grep -m1 '"cwd"' "$JSONL" 2>/dev/null)" || true
  cwd="$(jq -r '.cwd // ""' <<<"${hdr:-null}" 2>/dev/null)" || true
  branch="$(tail -n 400 "$JSONL" | grep '"gitBranch"' | tail -1 | jq -r '.gitBranch // ""' 2>/dev/null)" || true
  title="$(claude_title "$JSONL")"
  first_prompt="$(head -n 150 "$JSONL" | jq -r 'select(.type=="user") | .message.content | if type=="string" then . else ([.[]? | select(.type=="text") | .text] | join(" ")) end' 2>/dev/null | grep -v '^[[:space:]]*$' | grep -v '^Caveat' | grep -v '<command-' | grep -v '<local-command' | head -1 | cut -c1-200)" || true
  last_prompt="$(grep '"type":"last-prompt"' "$JSONL" 2>/dev/null | tail -1 | jq -r '(.lastPrompt // "") | .[0:200]' 2>/dev/null)" || true
else
  session_id="$(basename "$JSONL" .jsonl)"
  hdr="$(head -1 "$JSONL")" || true
  cwd="$(jq -r '.cwd // .payload.cwd // ""' <<<"${hdr:-null}" 2>/dev/null)" || true
  branch=""; title=""; first_prompt=""; last_prompt=""
fi

echo "Session: $session_id"
echo "Tool:    $TOOL"
echo "File:    $JSONL"
echo "Last activity: $(epoch_human "$e")"
[[ -n "${branch:-}" ]] && echo "Branch:  $branch"
[[ -n "${cwd:-}" ]]    && echo "cwd:     $cwd"
[[ -n "${title:-}" ]]  && echo "Title:   $title"
[[ -n "${first_prompt:-}" ]] && echo "First prompt: $first_prompt"
[[ -n "${last_prompt:-}" ]]  && echo "Last prompt:  $last_prompt"
(( skipped_active > 0 )) && echo "(skipped $skipped_active active session(s); resume.sh --list to see them)"
echo

# --- transcript extraction ------------------------------------------------------
format_turns() {
  jq -r '"[\(.r)] \(.t)\n" + (.x | if length > 2000 then .[0:2000] + "\n… (+\(length - 2000) chars truncated)" else . end) + "\n"'
}

print_turns_header() { # $1 = actual count shown
  if [[ "$ALL" == 1 ]]; then
    echo "— last $1 turns (incl. tool activity; asked for $N) —"
  else
    echo "— last $1 conversation turns (text only; asked for $N; --all for tool activity) —"
  fi
  echo
}

if [[ "$TOOL" == "claude" ]]; then
  recs="$(tail -n 4000 "$JSONL" | jq -c --arg all "$ALL" '
    select(.type=="user" or .type=="assistant") |
    select(.isSidechain != true) |
    (.message.content // "") as $c |
    { r: (.message.role // .type),
      t: ((.timestamp // "") | .[0:16] | sub("T"; " ")),
      x: (if ($c|type)=="string" then $c
          elif ($c|type)=="array" then
            ([$c[]? | if .type=="text" then (.text // "")
                      elif .type=="tool_use" then "⚙ \(.name // "?")"
                      else empty end] | join("\n"))
          else ($c|tostring) end) } |
    .x |= gsub("<system-reminder>.*?</system-reminder>"; ""; "s") |
    .x |= gsub("<local-command-caveat>.*?</local-command-caveat>"; ""; "s") |
    .x |= gsub("<local-command-stdout>.*?</local-command-stdout>"; ""; "s") |
    .x |= (if test("<command-name>") then "[command] " + (capture("<command-name>(?<c>[^<]*)</command-name>").c) else . end) |
    .x |= (if test("^Base directory for this skill: ") then "[skill] " + (try (.[0:300] | capture("skills/(?<s>[A-Za-z0-9._-]+)") | .s) catch "?") else . end) |
    .x |= gsub("^\\s+|\\s+$"; "") |
    select(.x != "") |
    select(.x | startswith("Caveat: The messages below") | not) |
    select(($all == "1") or (.x | startswith("⚙") | not))
  ' 2>/dev/null | tail -n "$N")" || true
  print_turns_header "$(printf '%s' "$recs" | grep -c . || true)"
  [[ -n "$recs" ]] && printf '%s\n' "$recs" | format_turns
elif [[ "$TOOL" == "codex" ]]; then
  out="$(tail -n 4000 "$JSONL" | jq -c '
    (.payload // {}) as $p |
    select(($p.type // .type // "") == "message") |
    { r: ($p.role // .role // "?"),
      t: ((.timestamp // "") | .[0:16] | sub("T"; " ")),
      x: (($p.content // .content // "") as $c |
          if ($c|type)=="string" then $c
          elif ($c|type)=="array" then ([$c[]? | (.text // empty)] | join("\n"))
          else ($c|tostring) end) } |
    .x |= gsub("^\\s+|\\s+$"; "") |
    select(.x != "") |
    select(.x | startswith("<user_instructions>") | not) |
    select(.x | startswith("<environment_context>") | not)
  ' 2>/dev/null | tail -n "$N")" || true
  if [[ -n "$out" ]]; then
    print_turns_header "$(printf '%s' "$out" | grep -c . || true)"
    printf '%s\n' "$out" | format_turns
  else
    echo "(structured extraction returned nothing — printing raw last $N lines)"
    tail -n "$N" "$JSONL"
  fi
else
  echo "(unknown tool layout — printing raw last $N lines)"
  tail -n "$N" "$JSONL"
fi
