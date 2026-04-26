---
argument-hint: "[tech-stack]"
description: Create comprehensive technical implementation plan from specification
---

# Implementation Plan Generator

Generate a detailed technical implementation plan from a specification document and create or analyze technology stack.

## Arguments

$1 (Optional: specific technology stack in Korean or English format)

## Instructions

1. **Read `docs/spec-init.md`**: Understand feature requirements and success criteria
2. **Determine Technology Stack**:
   - If user provides $1: Use specified technology stack
   - If not provided: Analyze project structure and recommend appropriate technologies
3. **Create `docs/plan-init.md`** with the following structure:
   - Original Tech Stack Request (record user input if provided)
   - Technology Stack (frameworks, libraries, versions for implementation)
   - Architecture Overview (high-level system design, component interactions)
   - Data Models (database schema, data structures, relationships)
   - API Design (endpoints, request/response formats if applicable)
   - Component Structure (component hierarchy, organization, folder structure)
   - State Management (data flow, store architecture)
   - Security Considerations (authentication, authorization, data protection)
   - Testing Strategy (unit, integration, E2E test approach)
   - Deployment Plan (build process, environment configuration, CI/CD)
   - Dependencies (packages, versions, compatibility notes)

4. **Generate Report**:
   - Summarize technology selection rationale
   - Explain key architectural decisions
   - Guide user to next step: run `/simple-sdd/tasks` to generate implementation tasks

## Quality Standards

- **Technical Feasibility**: All proposed solutions must be practically implementable
- **Specification Alignment**: Plan must precisely match requirements from spec-init.md
- **Implementation Detail**: Sufficiently detailed for developers to begin coding
- **Best Practices**: Incorporates industry standards and proven patterns
- **Scalability**: Considers future growth and maintenance

## Output Format

### Report Structure
1. **Selected Technology Stack** - List of frameworks and key libraries
2. **Architecture Highlights** - 3-5 key design decisions and their rationale
3. **Key Components** - Major components and their responsibilities
4. **Next Steps** - Instructions to run `/simple-sdd/tasks`

## Task

Based on the specification in `docs/spec-init.md` and optional technology preference in $1, create a comprehensive implementation plan. The plan should provide sufficient technical detail for experienced developers to begin implementation immediately.

Generate the plan following the Structure outline and ensure each section provides actionable guidance with specific technologies, patterns, and architectural decisions.

Write all content in the same language as the original specification document (Korean or English).
