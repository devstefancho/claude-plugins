# Decomposition — Examples

Concrete issue graphs. Generic; pair with the Layout section in [SKILL.md](SKILL.md).

## One spec → one parent + many sub-issues

```
specs/phase-2-auth/01-login.md          →  #201 login (parent)
                                             ├─ #202 로그인 화면 end-to-end        blocked-by: —
                                             └─ #203 세션 발급·저장 end-to-end     blocked-by: #202
specs/phase-2-auth/02-token-refresh.md  →  #210 token refresh (parent)
                                             └─ #211 만료 직전 자동 갱신           blocked-by: #203  (cross-spec)
```

- Each parent's body carries `spec: specs/phase-2-auth/01-login.md`; each spec's frontmatter carries `issue: owner/repo#201`.
- Ordering **between specs** is expressed as `blocked-by` across sub-issues (`#211 ← #203`), with the reason written in #211's dependency section.

## A small spec gets one issue, not a hierarchy

```
specs/phase-2-auth/03-logout-copy-fix.md  →  #215 로그아웃 문구 수정   (no parent, no sub-issues)
```

Creating a parent with a single child is noise. One issue, spec backlink in the body, done.

## A piece too small to be an issue

```
#202 로그인 화면 end-to-end
  body checklist:
    - [ ] 에러 문구 i18n 키 추가
    - [ ] 로딩 스피너 재사용 컴포넌트로 교체
```

These are steps inside one verifiable slice — they belong in the issue's checklist, not in the tracker as separate items.

## An issue must not span multiple specs

`spec:` is a single backlink, by design — the relation is **one parent issue : one spec** (and one spec : many sub-issues). If a piece of work seems to need two specs, that is a **boundary error**:

- Most often the spec boundary is wrong → re-scope the specs so the work falls under one, then decompose.
- Or the piece is too big → split it so each part maps to a single spec.
- Genuine ordering between specs is expressed with `blocked-by` and explained in the issue body — never by listing two specs.

There is no "multi-spec issue" form. Producing one means the decomposition skipped a boundary fix — stop and re-scope the specs first.

## Repo routing

| Situation | Where the issue goes |
|---|---|
| Work clearly belongs to one repo | that repo |
| Work spans repos, or the home isn't obvious in seconds | the meta tracker repo the user's routing rule designates, tagged with an area/app label |
| Not development work at all (research, decisions, personal todos) | not this skill's business — the user's routing rule decides |
