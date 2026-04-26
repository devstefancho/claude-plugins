---
argument-hint: "[requirements]"
description: "Generate a comprehensive software specification document from requirements"
---

# Specification Generator

Generate a detailed, structured software specification document from user-provided requirements.

## Arguments

$1 (Korean/English supported)

## Instructions

1. **Analysis**: Carefully analyze and clearly understand the provided requirements
2. **Document Generation**: Create `docs/spec-init.md` with the following structure:
   - Original Requirements (user input as-is)
   - Overview (brief summary)
   - Goals (clear objectives)
   - User Stories (user perspective scenarios)
   - Functional Requirements (what needs to be done)
   - Non-Functional Requirements (performance, security, accessibility)
   - Constraints & Assumptions (constraints and assumptions)
   - Success Criteria (success criteria)

3. **Report**: Summarize key content for the user and guide them to use `/simple-sdd/plan [tech-stack]` command

## Quality Standards

- **Clarity**: Clear, unambiguous, and complete specifications
- **Verifiability**: Testable and measurable requirements
- **Consistency**: Perfect alignment with user requirements

## Task

Based on the requirements provided in $1, create a comprehensive specification document that meets the quality standards above. The document should be written in the same language as the input (Korean or English).

Generate the specification following the Structure outline and ensure each section is detailed and actionable.
