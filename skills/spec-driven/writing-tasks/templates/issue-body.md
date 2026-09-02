# Issue Body Templates

Two skeletons. Fill and pass with `--body-file`; never paste a wall of spec prose into an issue.

## Parent issue (one per spec)

```markdown
spec: {SPEC_PATH}

## 목표
{1-2 sentences from the spec's Purpose — what "done" means for the whole spec}

## 분해
- [ ] #{SUB_1}  {title}
- [ ] #{SUB_2}  {title}

## 이 부모에서 직접 처리 (sub-issue로 쪼갤 만큼은 아닌 것)
- [ ] {small step}

## 완료 기준
- [ ] 모든 sub-issue close
- [ ] spec `status:` 갱신 (wip → done)
```

The `분해` list is written **after** the sub-issues exist (they need numbers). Creating the parent with a placeholder list and editing it once is fine; leaving placeholders behind is not.

## Sub-issue (one per verifiable slice)

```markdown
spec: {SPEC_PATH}
parent: #{PARENT}

## 왜 이 순서인가
- blocked-by #{DEP} — {reason. cross-spec/cross-repo면 반드시 이유를 적는다}
- (없으면) 선행 없음 — 독립 실행 가능

## 구현 체크리스트
- [ ] {file or logical unit}
- [ ] {…}

## 완료 기준
- [ ] 로컬 검증 절차 통과
- [ ] 자동화된 테스트 통과
- [ ] 관측 가능성(로그/메트릭/감사) 확인

## 리스크 / 메모
- {gotcha}
```

## Rules

- The body says **what and why**, not the whole spec — the spec link carries the detail.
- `blocked-by` reasons live in the body; the relation itself lives in the issue graph. Both, always.
- Never add a "status" or "progress %" line — that state belongs to the issue's open/closed status and its checklist.
