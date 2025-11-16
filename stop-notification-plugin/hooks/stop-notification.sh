#!/bin/bash

# Stop hook: Display macOS modal notification when Claude finishes working
# This hook runs when the main Claude Code agent has finished responding

# Read JSON input from stdin (not used for simple notification)
# input_data=$(cat)

# Display native macOS modal dialog
osascript -e 'display dialog "Claude가 작업을 완료했습니다" with title "Claude Code 작업 완료" buttons {"확인"} default button "확인" with icon note giving up after 3'

# Exit with success (non-blocking)
exit 0
