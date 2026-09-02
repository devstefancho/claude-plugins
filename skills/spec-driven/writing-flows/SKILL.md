---
name: writing-flows
description: "Writes single-scenario Flow documents under flows/<topic>/ — use case context, one Mermaid diagram (sequence or flowchart), step-by-step branches, and source file references — so how a service behaves end-to-end can be grasped at a glance. Use when user asks for a sequence diagram, user flow, use case doc, or mentions 시퀀스 다이어그램, 유저 플로우, 플로우 그려줘, 동작 흐름, 플로우 작성. Also trigger on intent like 어떻게 동작하는지 한눈에 보고 싶다, 동작 순서 정리해줘 — but not on simple code questions about a single function."
allowed-tools: Read, Write, Glob, Grep, Bash, SendMessage
context: fork
agent: general-purpose
---

# Writing Flows

Document how one scenario behaves at runtime as a **Flow** file under `flows/`. A Flow makes the order of operations and the branching visible at a glance — the thing specs, tasks, and ADRs can't show.

## Hard Rules

- **Template-driven.** Every Flow follows [templates/flow-template.md](templates/flow-template.md) exactly — four sections, no freestyle.
- **One Flow = one scenario.** A request spanning multiple scenarios becomes multiple Flow files.
- **Code is the source of truth.** When code exists, read it before drawing. Never draw from assumption what can be verified by exploration.
- **Never auto-modify existing Flows.** Propose the diff, wait for confirmation.
- **No derived index files.** Never create `flows/README.md` or `flows/INDEX.md` — the directory listing is the index.

## Directory Rules

- **Flow 루트를 먼저 정한다.** 사용자 전역 규칙(work-routing 류)이 이 repo 의 2급 문서를 외부 doc-root 로 보내면 Flow 루트는 `<doc-root>/<repo-name>/flows/` 이고, 아니면 프로젝트 루트의 `flows/` 다. 아래 규칙(topic 디렉토리, `NN-` 접두어, 인덱스 금지)은 정해진 루트를 기준으로 적용한다.
- Flows live in `flows/<topic>/NN-name.md` under that root — a closed-root dir; the directory-structure SSOT is `check-doc-structure/golden_manifest.py` (shared with `writing-specs`, `writing-tasks`, `scaffold-new-app`, `reconcile-docs`). Topic = coherent feature/domain (`auth`, `checkout`), the same axis as ADR-0001 — never phase numbers.
- Match the topic against existing `flows/*/` directories before creating a new one.
- `NN` is a 2-digit index within the topic, starting `01`. Filenames are lowercase-with-hyphens.

## Phase 1 — Search

1. `Glob flows/**/*.md` and check whether a Flow for this scenario already exists.
   - Exact scenario match → 부모 세션에 `SendMessage` 로 update / create new / cancel 을 묻고, 답이 없으면 update (기존 Flow 를 보존하며 갱신) 로 진행하고 보고에 적는다. 이 스킬은 fork 라 사용자에게 직접 물을 수 없다.
   - Existing Flow whose `## Source` files no longer exist (verify with `Glob`) → report as outdated; propose an update, never apply silently.
2. Locate the scenario in code: entry point (route/handler/command), the calls it makes, and where behavior branches. Follow the chain far enough to know every actor and every branch — guessing here produces a wrong diagram.
3. No relevant code (design-stage scenario)? Fall back to specs (`Glob specs/**/*.md`) or conversation context, and say so in the report.

## Phase 2 — Write

Read [templates/flow-template.md](templates/flow-template.md) and fill it strictly:

- **Context** — 2-3 sentences: the scenario, its trigger, the actors involved.
- **Diagram** — exactly one Mermaid diagram. `sequenceDiagram` when the story is interaction between components/services; `flowchart TD` when it is user-facing branching between screens/states. Never both, never other types.
- **Steps & Branches** — numbered happy path; attach branches and edge cases to the step where they diverge (`— 실패 시 → ...`).
- **Source** — the files the Flow was derived from, file paths only (no line numbers — they go stale). For design-stage Flows, list the spec or write `(design — no code yet)`.

Diagram and Steps must agree with each other and with the code. On update, preserve sections the user didn't ask to change.

## Phase 3 — Report

End with a short report: Action (Created/Updated), File (relative path), Scenario (H1), Basis (code files explored, or spec/conversation), and any outdated Flows found in Phase 1. One actionable next step (e.g. a neighboring scenario worth documenting).

## Anti-patterns

**WRONG:** drawing the diagram from the user's description while the code says otherwise.
**RIGHT:** explore the code first; if it contradicts the user's description, surface the difference and ask which one the Flow should capture.

**WRONG:** one giant Flow covering signup, login, and password reset.
**RIGHT:** three Flow files in `flows/auth/`, each one scenario.

## Boundaries

This skill only writes Flow files. Requirements belong to `writing-specs`, work breakdown to `writing-tasks`. It never modifies source code.

## 호출자에게

이 스킬은 fork 로 백그라운드에서 돈다. 완료 알림을 받고 파일을 확인한 뒤 다음 단계로 넘어간다. 기다리지 않으면 Phase 3 리포트가 세션 기록에서 사라진다(2026-08-18 실측: Flow 2개가 완성됐는데 부모는 6시간 뒤까지 몰랐다).
