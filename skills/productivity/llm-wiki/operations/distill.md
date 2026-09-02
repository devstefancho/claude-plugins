# operation: distill

inbox와 (워터마크 이후) journal에 **남아 있는** 캡처를 주제별로 묶어 페이지로 승격한다. **선택 작업이다** — 사용자가 "위키 정리"라고 시킬 때만 돈다. 메인 경로(ingest)는 distill 없이 완결되므로, 여기 올 것은 링크 park·짧은 메모 잔여뿐이다.

<refs>PRINCIPLES.md: capture-layers, secret-scan, dedup, merge-and-split, frontmatter, wikilink, bidirectional, page-types, slug-rules, immutability. + ingest.md의 4~8단계를 재사용.</refs>

## 1. 수집

- **inbox**: `{wiki_root}/inbox/**/*.md` 전부 Read (큐라 전량, 하위 폴더 포함 — 다른 작업이 트리째 부어 넣은 181개가 `inbox/*.md` 에 안 잡혀 "정리할 것 없음"으로 끝난 실측 2026-09-02).
- **journal 워터마크**:
  ```bash
  grep -oE '\[[0-9]{4}-[0-9]{2}-[0-9]{2}\] distill' {wiki_root}/wiki/log.md | tail -1
  ```
  이 날짜 **이후(초과)** 의 `journal/YYYY-MM-DD.md`만 Read (파일명이 날짜라 사전순 비교). distill 기록이 없으면 전부. 사용자가 "전체 다시"면 워터마크 무시.
- 수집 대상이 없으면 "정리할 새 캡처 없음" 보고 후 종료.

## 2. 클러스터링·매칭

- 수집 항목을 **주제별로 묶는다** — 흩어진 관련 메모·링크를 한 개념으로 수렴.
- 클러스터마다 `Grep {wiki_root}/wiki/pages/`로 기존 페이지 검색 → 신규 생성 vs 기존 병합 판단 (PRINCIPLES.md dedup). 병합이면 merge-and-split의 의미 단위 병합·분할 규칙을 따른다.
- 페이지 가치가 없는 잡음(단순 리마인더 등)은 **버림 후보**로 표시.

## 3. 계획 확인 (1회)

항목별이 아니라 **배치 계획을 한 번에** 사용자에게 확인:

> 🧩 distill 계획 (inbox {N} · journal {M}일치)
> - 신규: [[slug1]](concept), [[slug2]](entity) …
> - 병합: [[기존slug]] ← 항목 …
> - 버림: <제목> (사유)
>
> 진행할까요? 조정할 것 있나요?

## 4. 승격 (ingest 4~8 재사용)

확인된 클러스터마다 ingest.md 단계를 그대로:
- **4** 페이지 작성 → `wiki/pages/{type}/{today}-{slug}.md` (type은 page-types로 판단)
- **5** 엔티티/개념 페이지 갱신
- **6** 백링크 보강
- **7** index.md 갱신
- **8** overview.md 갱신 (전체 이해가 바뀔 때만)

provenance (PRINCIPLES.md capture-layers):
- **inbox 항목** → inbox 파일 자체를 `scripts/secret_scan.py`로 게이트(PRINCIPLES.md secret-scan)한 뒤 그 내용을 `raw/sources/{captured}-{slug}.md`로 확정(날짜 = inbox `captured`, 헤더는 ingest.md 2단계 형식). exit 3이면 마스킹/폐기 확인 후 확정, 그 다음 **inbox 파일 삭제**.
- **journal 유래** 페이지 → raw 복사 없이 페이지 본문/frontmatter에 `journal/YYYY-MM-DD` 출처만. **journal은 절대 건드리지 않음.**
- **버림**: inbox면 삭제(계획에서 확인됨), journal이면 그대로 둔다.

## 5. lint

```bash
scripts/lint_wiki.py {wiki_root} --json
```
`missing_backlink`·`broken_link`·`missing_source`가 0이 될 때까지 보강.

## 6. 로그 (배치)

```bash
cat <<EOF | scripts/append_log.py {wiki_root} distill "inbox {N} + journal {M}d → pages {P}"
- Created: [[slug1]], [[slug2]]
- Merged: [[slug3]]
- Dropped: {d}
EOF
```

## 7. 보고

> ✅ distill 완료 — 신규 {c}/병합 {m}/버림 {d}, inbox 비움. `index` 갱신 _(tags는 Dataview 자동)_.

<forbid>
- 자동 실행·스케줄(cron/launchd/loop)·"끝나면 알려줄게" 모니터 — 사용자 발화로만 돈다 (토큰 예측 불가)
- journal 수정/삭제 (immutability 5)
- inbox 내용 개정 (immutability 6 — distill의 소비 삭제만 허용)
</forbid>
