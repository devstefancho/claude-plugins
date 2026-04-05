---
name: implement-with-test
description: Implement code with tests from a spec file or direct request. Auto-detects test framework (jest, vitest, pytest, go test, cargo test) and follows existing project patterns. Use when user asks to implement a spec, build a feature with tests, code from a spec, or says "implement", "구현", "구현해줘", "테스트와 함께 구현", "스펙 구현", "implement this spec". Proactively trigger whenever the user wants to turn a specification or requirement into working code with tests.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, AskUserQuestion
context: main
agent: general-purpose
---

# Implement with Test

Implements planned work (spec files or user requests) into production code with accompanying tests. Detects the project's language, test framework, and coding conventions to produce code that fits naturally into the existing codebase.

## Principles

1. **Spec-first** - Never start coding without a clear understanding of what to build. If working from a spec file, parse its 4 sections (Purpose, Requirements, Approach, Verification). If working from a direct request, extract equivalent structured information first. This prevents aimless coding and scope creep.

2. **Pattern-follower** - The project already has conventions for imports, naming, directory structure, and test organization. Detect and follow them rather than imposing external conventions. Code that looks foreign to the project creates maintenance burden, even if it's technically correct.

3. **Test-alongside** - Write tests as part of the implementation, not as an afterthought. Each Verification item from the spec maps to at least one test. This ensures the tests actually verify what the spec intended, not just what happened to get implemented.

4. **Run-to-green** - After writing code and tests, run the test suite. If tests fail, diagnose and fix (up to 3 attempts). Do not report success until tests pass. A green test suite is the definition of "done."

5. **Minimal diff** - Only create or modify files necessary for the feature. Do not refactor surrounding code, add unrelated type annotations, or "improve" existing patterns. The goal is a focused, reviewable changeset.

## Workflow

### Phase 1: Input Resolution

Determine what to implement:

1. **Spec file provided as argument** → Read and parse the spec file directly
2. **No argument but `specs/` exists** → git diff로 변경된 스펙을 우선 감지:
   a. `git diff --name-only HEAD -- specs/` 로 새로 추가되거나 수정된 스펙 파일 확인
   b. untracked 파일도 확인: `git ls-files --others --exclude-standard specs/`
   c. 변경된 스펙이 1개 → 해당 스펙을 자동으로 선택하여 진행
   d. 변경된 스펙이 여러 개 → 변경된 스펙 목록만 보여주고 `AskUserQuestion`으로 선택 요청
   e. 변경된 스펙이 없으면 → 전체 `Glob specs/**/*.md` fallback하여 목록 표시
3. **Direct request (no spec)** → Extract structured information from the user's request:
   - Purpose: What needs to be done and why (1-2 sentences)
   - Requirements: Concrete requirements (3-5 bullets)
   - Approach: Technical approach (2-5 sentences)
   - Verification: Testable scenarios (2-5 bullets)
   - Confirm the extracted plan with the user before proceeding

After resolving input, display the parsed spec summary so the user can verify alignment.

### Phase 2: Project Reconnaissance

Scan the project to understand its conventions. This phase determines how to write code that fits in.

**Language & framework detection:**
- Check for `package.json`, `tsconfig.json`, `pyproject.toml`, `go.mod`, `Cargo.toml`, `pom.xml`
- Read the relevant config to understand dependencies and project type

**Test framework detection (in priority order):**
1. Check `package.json` for a `test` script — this tells you how tests are actually run
2. `vitest.config.*` or `vite.config.*` with test config → vitest
3. `jest.config.*` or `package.json` with `"jest"` key → jest
4. `pytest.ini`, `setup.cfg [tool:pytest]`, or `pyproject.toml [tool.pytest]` → pytest
5. `go.mod` → go test
6. `Cargo.toml` → cargo test
7. If no framework detected → ask the user via `AskUserQuestion`

**Existing test pattern analysis:**
- Run `Glob **/*.test.* **/*.spec.* **/test_* **/*_test.* **/__tests__/**`
- Read 1-2 existing test files to learn:
  - Import style (ES modules vs CommonJS, relative vs alias paths)
  - Assertion library (expect, assert, chai)
  - Test structure (describe/it nesting, flat test() calls, test class methods)
  - Setup/teardown patterns (beforeEach, fixtures, factories)
  - Mocking approach (jest.mock, vi.mock, unittest.mock, testify)
- Note the test file naming convention: `*.test.ts` vs `*.spec.ts` vs `test_*.py` vs `*_test.go`
- Note the test file location: colocated with source, `__tests__/` directory, or separate `tests/` directory

**Source code pattern analysis:**
- Identify the source directory structure (src/, lib/, app/, etc.)
- Read 1-2 existing source files similar to what will be implemented
- Note import patterns, export style, error handling conventions

### Phase 3: Implementation Planning

Based on the spec and reconnaissance:

1. List the production code files to create or modify, with brief descriptions
2. List the test files to create, following the detected naming convention and location pattern
3. Map each spec Verification item to the test(s) that will cover it

Display the file plan to the user as an informational summary (no confirmation needed — just transparency).

### Phase 4: Code Implementation

Write the production code:

- Follow the spec's Approach section for architecture and design decisions
- Match existing code patterns: import style, naming conventions, error handling
- Handle edge cases mentioned in the Requirements section
- Keep functions focused — each should do one thing well
- Add only necessary exports for testability

### Phase 5: Test Implementation

Write tests covering the spec's Verification section:

- Use the detected test framework and assertion library
- Follow existing test file patterns (structure, naming, imports)
- Write at least one test per Verification bullet point
- Name tests descriptively — someone reading the test name should understand what's being verified
- Include edge case tests when the Requirements mention them
- Use the same mocking/setup patterns found in existing tests
- Avoid over-mocking: test real behavior where practical

### Phase 6: Verification & Report

1. **Run tests** using the detected test command via `Bash`
   - For JS/TS: use the `test` script from package.json, or `npx vitest run` / `npx jest` with the specific test file
   - For Python: `python -m pytest {test_file}`
   - For Go: `go test ./{package}/...`
   - For Rust: `cargo test`

2. **Handle failures** (max 3 attempts):
   - Read the error output carefully
   - Distinguish between implementation bugs and test bugs
   - Fix the root cause, not the symptom
   - Re-run after each fix

3. **Generate report** using the template: [templates/report-template.md](templates/report-template.md)
   - Fill in all fields: source, title, files, test results, spec coverage
   - Output the completed report as the final message

## Error Handling

| Situation | Action |
|-----------|--------|
| No spec file found and no direct request | Ask user what to implement via `AskUserQuestion` |
| Test framework not detected | Ask user which framework to use |
| Existing tests use unfamiliar patterns | Follow patterns as-is; do not "modernize" |
| Tests fail after 3 fix attempts | Report the current state honestly with error details |
| Spec is ambiguous | Ask user to clarify before implementing |
