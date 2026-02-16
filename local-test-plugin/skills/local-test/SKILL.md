---
name: local-test
description: Symlink 기반 로컬 플러그인 테스트 - 설치/해제 없이 개발 디렉토리를 직접 연결
allowed-tools: Bash, AskUserQuestion
context: fork
agent: general-purpose
---

# Local Test Skill

로컬 플러그인 개발 시 symlink로 캐시에 직접 연결하여, 파일 수정 → Claude Code 재시작만으로 변경사항을 테스트할 수 있게 합니다.

## 동작 흐름

### Step 1: marketplace.json에서 플러그인 목록 추출

마켓플레이스 루트의 `.claude-plugin/marketplace.json`에서 사용 가능한 플러그인 목록을 읽습니다.

```bash
MARKETPLACE_ROOT=$(cd "$(dirname "$0")/../../" && pwd)
```

실제로는 이 스킬이 설치된 위치와 무관하게, `/Users/stefancho/works/claude-plugins` 레포를 마켓플레이스 루트로 사용합니다.
Bash 도구로 `jq`를 사용하여 marketplace.json의 plugins[].name 목록을 추출하세요.

### Step 2: link/unlink 선택

AskUserQuestion으로 사용자에게 물어봅니다:
- **link**: 로컬 개발 디렉토리를 symlink로 연결
- **unlink**: symlink 해제하고 원래 캐시로 복원

### Step 3: 대상 플러그인 선택

AskUserQuestion으로 Step 1에서 추출한 플러그인 목록을 옵션으로 제시합니다.
(옵션이 4개를 초과하면 "Other"로 직접 입력할 수 있음을 안내)

### Step 4: 스크립트 실행

```bash
bash /Users/stefancho/works/claude-plugins/local-test-plugin/scripts/local-install.sh {link|unlink} {plugin-name}
```

### Step 5: 결과 안내

스크립트 실행 결과를 확인하고 사용자에게 안내합니다:
- 성공 시: "Claude Code를 재시작하면 변경사항이 반영됩니다."
- 실패 시: 에러 메시지와 해결 방법 안내
