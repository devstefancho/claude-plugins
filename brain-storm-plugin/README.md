# Brain Storm Plugin

현재 코드베이스를 기반으로 미래 기능과 개선 아이디어를 브레인스토밍합니다. UI 아이디어에는 ASCII wireframe을 포함하고, 이미 구현된 아이디어는 자동 감지하여 정리합니다.

## Installation

```bash
/plugin install brain-storm-plugin@devstefancho-claude-plugins
```

## Trigger Keywords

- 한국어: "브레인스톰", "아이디어", "기능 제안", "개선 아이디어", "뭐 만들까", "앞으로 뭐 하지"
- English: "brainstorm", "feature ideas", "what could we build", "improvement ideas"

## How It Works

1. **Codebase Scan** - 프로젝트 구조와 기존 아이디어 파악
2. **Ideation** - 3-5개 아이디어 생성 (복잡도 + UI 태그 포함)
3. **Deduplication** - 기존 아이디어와 중복 체크
4. **Write** - 선택된 아이디어를 템플릿으로 저장 (UI면 wireframe 포함)
5. **Implementation Check** - 이미 구현된 아이디어 감지 후 사용자 확인 하에 삭제
6. **Report** - 결과 요약 리포트 출력

## Directory Structure

```
brain-storm/
├── dashboard-analytics.md
├── auth/
│   └── sso-login.md
└── ui/
    └── dark-mode-toggle.md
```

- 파일은 `brain-storm/`에 저장, 최대 1-depth 하위 디렉토리 허용
- 파일명은 lowercase-with-hyphens 형식

## writing-specs와의 차이

| writing-specs | brain-storm |
|---------------|-------------|
| 구현할 것을 명세 | 구현할 수 있는 것을 탐색 |
| 구체적 요구사항 | 탐색적 아이디어 |
| Wireframe 없음 | UI 아이디어에 ASCII wireframe 포함 |
| Outdated 감지 | 구현 완료 감지 및 정리 |
