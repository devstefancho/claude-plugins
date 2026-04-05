# Computer Use Plugin

Computer Use MCP를 활용한 앱 테스트 자동화 스킬. 시나리오 기반 테스트 + ad-hoc 탐색으로 기능/UI·UX 이슈를 발견하고 구조화된 피드백 리포트를 생성한다.

## Installation

```bash
/plugin install computer-use-plugin@devstefancho-claude-plugins
```

## Prerequisites

- Computer Use MCP가 `/mcp`에서 활성화되어 있어야 함

## Trigger Keywords

- 한글: "computer use 테스트", "앱 테스트", "UI 테스트", "앱 QA"
- 영문: "computer use test", "cu test", "app test"

## How It Works

1. **Setup** - 대상 앱 확인, Computer Use MCP 권한 요청
2. **Scenario Preparation** - 기존 시나리오 확인 또는 신규 생성
3. **Scenario Execution** - 각 스텝을 Computer Use로 실행하며 이슈 탐지
4. **Ad-hoc Exploration** - 시나리오 외 자유 탐색으로 추가 이슈 발견
5. **Report** - 구조화된 피드백 리포트 생성

## Output Structure

```
test-cases/
└── {app-name}/
    ├── scenario-basic-flow.md
    ├── scenario-error-handling.md
    └── reports/
        └── 2026-04-05-report.md
```

## Templates

- `scenario-template.md` - 테스트 시나리오 (App, Preconditions, Steps)
- `feedback-template.md` - 개별 이슈 항목 (Severity, Category, Description, Screenshot)
- `report-template.md` - 최종 리포트 (Summary, Issues, Ad-hoc Exploration, Recommendations)
