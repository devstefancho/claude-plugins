# implement-with-test-plugin

Implement a task into code with tests. Auto-detects your project's test framework and follows existing coding conventions.

## Installation

```bash
/plugin install implement-with-test-plugin@devstefancho-claude-plugins
```

## Usage

Task 정보는 두 가지 방식으로 주입됩니다:

### 1. Argument (task 파일 경로 또는 설명)

Task 파일 경로:
```
specs/jwt-authentication.md 구현해줘
tasks/rate-limiter.md implement
```

직접 설명:
```
사용자 인증 미들웨어 구현해줘. JWT 토큰을 검증하고 req.user에 decode된 payload를 붙여야 함. 실패 시 401.
```

### 2. 현재 대화 기반

별도 argument 없이 트리거되면 최근 대화 맥락에서 task를 추출해 확인 후 진행합니다.

### Trigger keywords
- "implement", "구현", "구현해줘"
- "테스트와 함께 구현"

## Supported Test Frameworks

| Framework | Detection |
|-----------|-----------|
| vitest | `vitest.config.*` |
| jest | `jest.config.*` or package.json `jest` key |
| pytest | `pytest.ini`, `pyproject.toml [tool.pytest]` |
| go test | `go.mod` |
| cargo test | `Cargo.toml` |

## Workflow

1. **Task Resolution** — argument(파일 경로 or 설명) 또는 현재 대화에서 task 추출 (Purpose / Requirements / Approach / Verification)
2. **Project Reconnaissance** — 언어, 테스트 프레임워크, 코딩 컨벤션 감지
3. **Implementation Planning** — 생성/수정 파일 계획
4. **Code Implementation** — 기존 패턴을 따르는 프로덕션 코드 작성
5. **Test Implementation** — Verification 항목을 커버하는 테스트 작성
6. **Verification & Report** — 테스트 실행 및 5-섹션 구조 리포트 출력
7. **Task Document Update** — argument가 파일 경로였을 경우, 해당 문서의 `status` / `completed_at` frontmatter와 Verification 체크리스트를 surgical하게 갱신

## Report Output Format

작업 완료 시 다음 5개 섹션으로 구조화된 리포트를 출력합니다:

- **완료한 기능** — 사용자 관점에서 가능해진 외부 동작
- **기술 구현** — 변경 파일, 주요 설계 결정
- **테스트** — 프레임워크, 실행 결과, 커버리지 매핑
- **사용자 조치 필요** — 환경 설정, 마이그레이션 등 수동 작업 항목
- **다음 단계** — 후속 작업 1-3개
