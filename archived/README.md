# Archived Plugins

마켓플레이스에서 등록 해제하고 이 디렉토리로 옮긴 플러그인 모음. 코드 자체는 보존하지만 `/plugin install`로 설치할 수 없다 (`marketplace.json`에서 제거됨).

## 보존하는 이유

- 과거 작업 컨텍스트 유지 (히스토리·이슈·README 추적)
- 필요 시 일부 로직을 새 플러그인으로 가져오기 쉬움
- 완전 삭제 대신 격리해 마켓을 깔끔하게 유지

## 어디서 무엇으로 대체되는가

| 플러그인 | 대체재 / 사유 |
|---|---|
| code-style-plugin | impeccable + codex |
| code-quality-plugin | impeccable + codex |
| frontend-plugin | impeccable |
| simple-sdd-plugin | writing-specs-plugin + writing-tasks-plugin + implement-with-test-plugin |
| spec-manager-plugin | writing-specs-plugin |
| smart-commit-plugin | impeccable + codex |
| git-commit-plugin | `commit-commands:commit` (official) |
| pr-create-plugin | `commit-commands:commit-push-pr` (official) |
| git-worktree-plugin | agent-team-plugin이 wraps |
| session-reporter-plugin | wiki-sync (user skill) |
| worktrace-plugin | wiki-sync |
| work-journal-plugin | wiki에 흡수 (`.gitignore`된 상태로 보존) |
| common-mcp-plugin | 사용 안 함 |
| scaffold-claude-feature | 사용 안 함 |
| local-test-plugin | `--plugin-dir` 플래그로 대체 |

## 복원이 필요하면

1. 해당 디렉토리를 `archived/`에서 루트로 `git mv`
2. `.claude-plugin/marketplace.json`의 `plugins` 배열에 항목 다시 추가
3. plugin.json `version` 한 단계 올림 (캐시 무효화)
