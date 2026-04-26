# browser-walkthrough-plugin

playwright-cli **headed 모드**로 브라우저를 같이 보면서 한 스텝씩 대화형으로 진행하는 워크플로우. 홈택스·정부24·은행·쇼핑몰처럼 iframe·보안프로그램·팝업이 많은 사이트를 사용자와 함께 진행할 때 사용.

## 전제 조건 (사전 설치 필요)

이 플러그인은 별도 `playwright-cli` 스킬에 의존한다. 본 플러그인에 묶지 않은 이유: playwright-cli는 외부에서 활발히 갱신되고 다른 플러그인(impeccable, frontend-design 등)도 동일 스킬을 가져오므로, 묶으면 본가 업데이트가 끊긴다.

설치 옵션:
- 가장 간단: 외부 플러그인(예: `frontend-design`, `impeccable`) 설치 시 `playwright-cli` 스킬이 함께 따라옴
- 또는 user-level에 직접 두기: `~/.claude/skills/playwright-cli/`

`playwright-cli`가 사용 가능한 상태인지 먼저 확인 후 본 플러그인을 사용하라.

## 사용법

자연어 트리거:
- "브라우저 보면서 같이 진행"
- "홈택스 같이 / 정부24 같이"
- "step-by-step browser" / "한 스텝씩"

## 대화 프로토콜 (요약)

| 입력 | 행동 |
|---|---|
| `다음`, `next`, `진행`, `ok` | 직전 제안 액션 실행 → snapshot → 다음 스텝 |
| `뒤로` | go-back |
| `잠깐`, `wait` | 액션 금지, 대기 (사용자 수동 조작 중) |
| 구체적 값 | 직전 필드에 fill |
| 질문 | 답변만 하고 대기 |
| `ok 제출`, `결제 진행` | 위험 액션 게이트 통과 |
| `완료`, `끝` | 후속 액션 아이템 요약 |

## Install

```bash
/plugin marketplace add devstefancho/claude-plugins
/plugin install browser-walkthrough-plugin@devstefancho-claude-plugins
```
