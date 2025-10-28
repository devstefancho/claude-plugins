# Development Marketplace

로컬 개발 환경에서 code-style-plugin을 테스트하기 위한 마켓플레이스입니다.

## 구조

```
dev-marketplace/
├── .claude-plugin/
│   └── marketplace.json        # 마켓플레이스 메타데이터
├── code-style-plugin/          # 플러그인 소스 (심볼릭 링크)
└── README.md
```

## 설정

### 1. 마켓플레이스 추가

```bash
cd /Users/stefancho/works/claude-plugins
claude /plugin marketplace add ./dev-marketplace
```

### 2. 설치 가능한 플러그인 확인

```bash
/plugin
```

"Browse Plugins"를 선택하여 code-style-plugin을 볼 수 있습니다.

### 3. 플러그인 설치

```bash
/plugin install code-style-plugin@dev-marketplace
```

Claude Code 재시작 후 설치가 완료됩니다.

## 개발 워크플로우

### 플러그인 수정

1. `../code-style-plugin/` 디렉토리의 파일 수정
2. Claude Code 재시작
3. Skill 변경사항 확인

### 테스트

```
코드를 리뷰해줄래? @src/example.ts
```

## 마켓플레이스 파일 구조

### marketplace.json

```json
{
  "name": "dev-marketplace",
  "description": "...",
  "owner": { "name": "..." },
  "plugins": [
    {
      "name": "code-style-plugin",
      "source": "../code-style-plugin",
      "description": "..."
    }
  ]
}
```

- **name**: 마켓플레이스 ID (설치 시 @dev-marketplace로 사용)
- **source**: 플러그인 소스 경로 (상대 경로)
- **plugins**: 마켓플레이스에서 제공하는 플러그인 목록

## 기타

더 자세한 내용은 `../code-style-plugin/README.md` 참고
