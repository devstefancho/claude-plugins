---
argument-hint: "[--all]"
description: "Implement features from tasks document with optional batch mode"
model: claude-haiku-4-5-20251001
---

# Implementation Executor

Execute implementation tasks from the task breakdown document, with support for batch or incremental implementation.

## Arguments

`--all` (optional, batch implementation flag)

## Instructions

1. **Read Required Documents**:
   - Read `docs/tasks-init.md` to understand all tasks and their organization
   - Read `docs/spec-init.md` to understand requirements and success criteria
   - Read `docs/plan-init.md` to understand technical decisions and architecture

2. **Implementation Strategy**:
   - If `--all` flag is provided: Implement all tasks in batch mode
   - If `--all` flag is NOT provided: Implement tasks by group, then wait for user approval before proceeding to next group

3. **For Each Task**:
   - Mark task as in_progress using TodoWrite
   - Implement the feature following:
     - Existing code patterns and conventions
     - Technical decisions from plan-init.md
     - Specification requirements from spec-init.md
   - Write clean, maintainable code
   - Test functionality to ensure it works correctly
   - Mark task as completed using TodoWrite immediately after successful completion

4. **Code Quality Standards**:
   - Follow existing code style and patterns in the codebase
   - Use consistent naming conventions
   - Write clear, self-documenting code
   - Handle edge cases appropriately
   - Ensure no breaking changes to existing functionality

5. **Testing During Implementation**:
   - Manual testing: Verify each feature works as specified
   - Test normal use cases first, then edge cases
   - Ensure error handling works correctly
   - Document any test steps performed

6. **Completion Report**:
   After all tasks (or all groups if using incremental mode) are complete, provide:
   - Summary of implemented features
   - List of created or modified files
   - Detailed testing methodology:
     * Manual test steps with expected results
     * Test command examples (if applicable)
     * Edge cases covered
   - Next steps guidance (for --all: done; for incremental: ready for next group)

## Quality Standards

- **Code Quality**: Clean, readable code following project conventions
- **Specification Alignment**: All implementations match requirements from spec-init.md
- **Technical Adherence**: Solutions follow architecture and decisions from plan-init.md
- **Testing Coverage**: Manual testing validates all requirements and edge cases
- **Error Handling**: Proper error handling and edge case management
- **Documentation**: Clear test procedures and expected results

## Task

Read the tasks from `docs/tasks-init.md`, specification from `docs/spec-init.md`, and technical plan from `docs/plan-init.md`. Then implement all tasks following the instructions above.

The implementation should result in a fully functional feature set that meets all specification requirements, passes all manual testing, and maintains code quality standards. Each task must be atomic, testable, and contribute to achieving the specification goals.

If implementing incrementally (without --all), wait for user approval after completing each task group before proceeding to the next group.
