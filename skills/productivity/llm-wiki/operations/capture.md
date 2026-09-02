# operation: capture

짧은 메모와 나중에 볼 링크를 마찰0으로 캡처 계층(`journal/`·`inbox/`)에 떨군다. **받아 적기만 한다** — 분류·페이지화·컴파일은 하지 않는다. 대화 요약·리서치처럼 페이지가 돼야 하는 것은 capture가 아니라 **ingest**다(같은 턴에 raw+pages).

<refs>PRINCIPLES.md: capture-layers, slug-rules (inbox 파일명용).</refs>

## 0. 디렉토리 보장

```bash
mkdir -p {wiki_root}/journal {wiki_root}/inbox
```

`{today}`=`date +%F`, `{now}`=`date +%H:%M`.

## 1. 대상 계층 결정

발화로 분기 (모호하면 journal 기본):

| 입력 | 대상 |
|---|---|
| 즉흥 생각·"메모"·"적어둬"·짧은 노트 | journal |
| 나중에 볼 링크/URL·처리 대기 자료 한 줄 | inbox |
| "이 대화 정리"·대화 요약·외부 자료 소화 | **capture 아님 → ingest로 안내** (ingest.md 1c) |

## 2a. journal append (대상=journal)

파일 `{wiki_root}/journal/{today}.md`. 느슨한 포맷 — 옵시디언에서 직접 쓴 것과 섞여도 되게 강제 구조 없음.

1. 파일이 있으면 Read, 없으면 `# {today}`로 시작.
2. 끝에 다음 블록을 붙여 Write (append):
   ```
   ## {now}
   {메모 원문 — 합성·편집 없이 그대로. URL은 마크다운 링크로 둠}
   ```

요약하지 않는다. 사용자가 쓴 그대로 보존.

## 2b. inbox 항목 생성 (대상=inbox)

slug는 PRINCIPLES.md slug-rules로 생성. `{wiki_root}/inbox/{today}-{slug}.md`에 Write:

```
---
captured: {today}
kind: link | note
source: <url · (직접입력)>
---

{내용}
```

- **링크**: URL + 한 줄 메모만 park. 본문 fetch·요약·컴파일 금지 (그건 ingest). `kind: link`.
- **처리 대기 자료**: 사용자가 준 짧은 텍스트 그대로. `kind: note`.
- 시크릿(API키·토큰·비밀번호)은 옮겨 적지 않는다.

## 3. 보고 (한 줄)

> 📥 캡처됨 → `journal/{today}.md` _(또는 `inbox/{today}-{slug}.md`)_. inbox는 "위키 정리"라고 시킬 때 distill이 묶는다(자동 아님).

**로그 남기지 않음.** capture는 고빈도라 `log.md`를 채우지 않는다 — 정리 이력은 distill이 배치로 기록한다.
