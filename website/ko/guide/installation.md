# 설치 가이드

플러그인 설치 및 관리에 대한 상세 가이드입니다.

## 마켓플레이스 관리

### 마켓플레이스 등록

```bash
/plugin marketplace add devstefancho/claude-plugins
```

### 등록된 마켓플레이스 확인

```bash
/plugin
# 'devstefancho-claude-plugins' 마켓플레이스가 표시됩니다
```

## 대체 방법: npx skills

[Vercel Skills CLI](https://github.com/vercel-labs/skills)를 사용하여 일반 터미널에서 스킬을 설치할 수 있습니다:

```bash
# 사용 가능한 스킬 목록 확인
npx skills add devstefancho/claude-plugins --list

# 모든 스킬 설치
npx skills add devstefancho/claude-plugins

# 특정 스킬 설치
npx skills add devstefancho/claude-plugins --skill code-style-reviewer

# 전역 설치 (사용자 전체)
npx skills add devstefancho/claude-plugins -g
```

> 참고: `npx skills`는 Agent Skills만 설치합니다. Commands, Hooks, MCP Servers는 아래의 `/plugin install` 방법을 사용하세요.

## 플러그인 설치

### 단일 플러그인 설치

```bash
/plugin install <plugin-name>@devstefancho-claude-plugins
```

### 추천 플러그인 조합

**코드 리뷰 세트**
```bash
/plugin install code-style-plugin@devstefancho-claude-plugins
/plugin install code-quality-plugin@devstefancho-claude-plugins
```

**Git 워크플로우 세트**
```bash
/plugin install git-commit-plugin@devstefancho-claude-plugins
/plugin install pr-create-plugin@devstefancho-claude-plugins
/plugin install git-worktree-plugin@devstefancho-claude-plugins
```

**개발 생산성 세트**
```bash
/plugin install scaffold-claude-feature@devstefancho-claude-plugins
/plugin install session-reporter-plugin@devstefancho-claude-plugins
/plugin install stop-notification-plugin@devstefancho-claude-plugins
```

## 플러그인 해제

```bash
/plugin uninstall <plugin-name>@devstefancho-claude-plugins
```

## 설치 후 체크리스트

1. ✅ Claude Code 재시작 (터미널 닫고 다시 열기)
2. ✅ `/plugin` 명령어로 설치 확인
3. ✅ `/help` 명령어로 새 명령어 확인 (Commands 플러그인의 경우)
4. ✅ Skills는 자동으로 감지되어 활성화됨

## 문제 해결

### 플러그인이 작동하지 않는 경우

1. Claude Code를 완전히 재시작했는지 확인
2. `/plugin` 명령어로 플러그인이 설치되었는지 확인
3. 플러그인 버전 호환성 확인

### 마켓플레이스 등록 실패 시

```bash
# GitHub 접근 권한 확인
git ls-remote https://github.com/devstefancho/claude-plugins.git
```

## 팀 공유

팀 프로젝트의 `.claude/settings.json`에 마켓플레이스를 추가하여 자동으로 공유할 수 있습니다:

```json
{
  "plugins": {
    "marketplaces": ["devstefancho/claude-plugins"]
  }
}
```
