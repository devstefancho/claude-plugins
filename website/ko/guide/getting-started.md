# 시작하기

Claude Plugins 마켓플레이스에 오신 것을 환영합니다!

## Claude Plugins란?

Claude Plugins는 Claude Code CLI를 확장하는 재사용 가능한 컴포넌트들의 모음입니다:

- **Skills**: Claude Code가 자동으로 활성화하는 전문 지식 및 동작
- **Commands**: `/` 로 시작하는 커스텀 슬래시 명령어
- **Hooks**: 특정 이벤트에 반응하는 자동화 스크립트
- **MCP Servers**: 외부 도구와의 통합

## 사전 요구사항

- Claude Code CLI가 설치되어 있어야 합니다
- Git 접근 권한이 필요합니다

## 빠른 시작

### 1. 마켓플레이스 등록

```bash
/plugin marketplace add devstefancho/claude-plugins
```

### 2. 플러그인 설치

```bash
# 예: 코드 스타일 리뷰 플러그인
/plugin install code-style-plugin@devstefancho-claude-plugins

# 예: Git 커밋 자동화 플러그인
/plugin install git-commit-plugin@devstefancho-claude-plugins
```

### 3. Claude Code 재시작

플러그인 설치 후 Claude Code를 재시작해야 적용됩니다.

```bash
# 터미널을 닫고 다시 열거나
# 새로운 Claude Code 세션 시작
claude
```

### 4. 설치 확인

```bash
/plugin
# 설치된 플러그인 목록 확인
```

## 다음 단계

- [설치 가이드](/ko/guide/installation) - 상세한 설치 방법
- [플러그인 목록](/ko/plugins/) - 모든 플러그인 둘러보기
