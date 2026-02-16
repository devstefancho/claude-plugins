# local-test-plugin

Symlink 기반 로컬 플러그인 테스트 도구. 플러그인 개발 시 uninstall/install 사이클 없이 파일 수정 → Claude Code 재시작만으로 변경사항을 바로 테스트할 수 있습니다.

## 설치

```bash
/plugin install local-test-plugin@devstefancho-claude-plugins
```

## 사용법

### 스킬로 실행

Claude Code에서 `local-test`를 트리거하면 대화형으로 안내합니다:

1. link/unlink 선택
2. 대상 플러그인 선택 (marketplace.json 기반)
3. 자동 실행 및 결과 안내

### 스크립트 직접 실행

```bash
# 로컬 디렉토리를 symlink로 연결
bash local-test-plugin/scripts/local-install.sh link <plugin-name>

# symlink 해제하고 원래 상태로 복원
bash local-test-plugin/scripts/local-install.sh unlink <plugin-name>
```

### 예시

```bash
# git-worktree-plugin을 로컬 개발 모드로 전환
bash local-test-plugin/scripts/local-install.sh link git-worktree-plugin

# 파일 수정 후 Claude Code 재시작하면 변경사항 반영됨

# 원복
bash local-test-plugin/scripts/local-install.sh unlink git-worktree-plugin
```

## 동작 원리

### link

1. 대상 플러그인이 설치되어 있는지 확인
2. 로컬 `plugin.json`에서 dev 버전 추출
3. 기존 캐시 디렉토리를 `.bak`으로 백업
4. symlink 생성: `~/.claude/plugins/cache/.../plugin-name/version/` → 로컬 디렉토리
5. `installed_plugins.json` 백업 후 경로/버전 업데이트

### unlink

1. `installed_plugins.json.bak`에서 원래 정보 복원
2. symlink 제거
3. `.bak` 캐시 디렉토리를 원래 이름으로 복원

## 전제 조건

- `jq` 설치 필요 (`brew install jq`)
- 대상 플러그인이 이미 `/plugin install`로 설치되어 있어야 함
- 마켓플레이스 레포가 로컬에 clone되어 있어야 함
