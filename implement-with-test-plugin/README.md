# implement-with-test-plugin

Implement code with tests from spec files or direct requests. Auto-detects your project's test framework and follows existing coding conventions.

## Installation

```bash
/plugin install implement-with-test-plugin@devstefancho-claude-plugins
```

## Usage

### From a spec file (writing-specs-plugin)
```
specs/jwt-authentication.md 구현해줘
```

### Direct request
```
사용자 인증 미들웨어를 구현하고 테스트도 작성해줘
```

### Trigger keywords
- "implement", "구현", "구현해줘"
- "테스트와 함께 구현", "스펙 구현"
- "implement this spec"

## Supported Test Frameworks

| Framework | Detection |
|-----------|-----------|
| vitest | `vitest.config.*` |
| jest | `jest.config.*` or package.json `jest` key |
| pytest | `pytest.ini`, `pyproject.toml [tool.pytest]` |
| go test | `go.mod` |
| cargo test | `Cargo.toml` |

## Workflow

1. **Input Resolution** - Parse spec file or extract requirements from direct request
2. **Project Reconnaissance** - Detect language, test framework, and coding conventions
3. **Implementation Planning** - Determine files to create/modify
4. **Code Implementation** - Write production code following existing patterns
5. **Test Implementation** - Write tests covering spec's Verification items
6. **Verification & Report** - Run tests, fix failures, output structured report
