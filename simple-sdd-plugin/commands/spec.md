---
argument-hint: "[requirements]"
description: "Generate a comprehensive software specification document from requirements"
model: claude-haiku-4-5-20251001
---

# Specification Generator

Generate a detailed, structured software specification document from user-provided requirements.

## Arguments

$1 (Korean/English supported)

## Instructions

1. **분석**: 제공된 요구 사항을 세밀하게 분석하고 명확히 이해
2. **문서 생성**: 다음 구조로 `docs/spec-init.md` 생성:
   - Original Requirements (사용자 입력 그대로)
   - Overview (간단한 요약)
   - Goals (명확한 목표)
   - User Stories (사용자 관점 시나리오)
   - Functional Requirements (해야 할 일)
   - Non-Functional Requirements (성능, 보안, 접근성)
   - Constraints & Assumptions (제약사항과 가정)
   - Success Criteria (성공 기준)

3. **보고**: 핵심 내용을 요약해서 사용자에게 제시하고, `/simple-sdd/plan [tech-stack]` 명령 사용 안내

## Quality Standards

- **명확성**: 명확하고 모호하지 않으며 완전한 명세
- **검증성**: 테스트 가능하고 측정 가능한 요구 사항
- **정합성**: 사용자 요구 사항과 완벽하게 일치

## Task

Based on the requirements provided in $1, create a comprehensive specification document that meets the quality standards above. The document should be written in the same language as the input (Korean or English).

Generate the specification following the Structure outline and ensure each section is detailed and actionable.
