---
argument-hint: "[context]"
description: Generate implementation tasks from specification and plan
---

# Tasks Generator

Generate detailed, atomic implementation tasks from specification and technical plan documents.

## Arguments

$1 (Optional: additional context or task filtering in Korean/English)

## Instructions

1. **Read Documents**:
   - Read `docs/spec-init.md` to understand all requirements and success criteria
   - Read `docs/plan-init.md` to understand technical architecture and implementation strategy

2. **Generate `docs/tasks-init.md`** with the following structure:
   - **Task Groups**: Organize tasks by logical categories (e.g., Setup & Configuration, Database & Data Models, API Endpoints, Frontend Components, Integration & Testing)
   - **Task Format**: Each task must include:
     - ID: **T-001**, **T-002** format (sequential numbering)
     - Title: Clear, concise task name
     - Purpose: Why this task is needed
     - Description: What needs to be implemented
     - Dependencies: Reference other task IDs if applicable
     - Required: Yes/No (critical for MVP vs. enhancements)
   - **Task Characteristics**:
     - Atomic: Each task should be completable in 1-3 hours
     - Testable: Clear acceptance criteria
     - Ordered: Tasks sorted by dependencies and logical flow
   - **Report Section**: Include summary statistics

3. **Generate Report**:
   - Total number of tasks and groups
   - Each group name with complexity rating (Low/Medium/High)
   - Summary table: Task ID, Title, Purpose (brief), Required (Yes/No)
   - Key insights about task distribution
   - Next steps: Guide user to run `/implement [--all]` to begin implementation

## Quality Standards

- **Specification Alignment**: All tasks derived from spec-init.md requirements
- **Plan Adherence**: Tasks follow technical architecture from plan-init.md
- **Atomic & Testable**: Each task is small and has clear acceptance criteria
- **Dependency Management**: Tasks ordered correctly with dependencies documented
- **Realistic Scope**: Tasks are achievable and well-scoped
- **Complete Coverage**: All aspects of spec and plan are covered

## Task

Based on the specification in `docs/spec-init.md` and technical plan in `docs/plan-init.md`, create a comprehensive task breakdown that developers can immediately begin implementing.

Generate the tasks following the Structure outline with proper grouping, sequencing, and detailed descriptions. Ensure every task is atomic, testable, and clearly linked to specification requirements.

Write all content in English and follow the exact formatting specified above.
