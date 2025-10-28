# Code Style Plugin

코드 스타일 원칙 기반 AI 코드 리뷰 플러그인입니다. Claude가 직접 코드를 분석하여 5가지 핵심 원칙을 중심으로 상세한 리뷰를 제공합니다.

## 🎯 기능

이 플러그인은 다음 5가지 핵심 원칙으로 코드를 검사합니다:

1. **단일책임원칙 (SRP)** - 함수/클래스는 하나의 책임만 가져야 합니다
2. **DRY** - 반복되는 코드를 피하고 공통 로직을 추출합니다
3. **단순화 우선** - 복잡한 추상화보다 이해하기 쉬운 코드를 선호합니다
4. **YAGNI** - 현재 필요하지 않은 기능은 구현하지 않습니다
5. **타입 안전성** - `any` 타입을 피하고 명확한 타입을 정의합니다

추가로 다음도 검사합니다:
- 명명규칙 (변수, 함수, 클래스 등의 일관성)
- 코드 구조 및 복잡도
- 주석 및 문서화 품질

## 📦 설치

### 1. Local Marketplace 추가

```bash
cd /Users/stefancho/works/claude-plugins
claude /plugin marketplace add ./dev-marketplace
```

### 2. Plugin 설치

```bash
/plugin install code-style-plugin@dev-marketplace
```

설치 후 Claude Code를 재시작하면 플러그인이 활성화됩니다.

## 🚀 사용 방법

### 자동 사용

코드 리뷰 관련 요청을 하면 Claude가 자동으로 이 Skill을 사용합니다:

```
"이 코드를 리뷰해줄래?"
"이 함수의 코드 품질을 분석해줘"
"코드 구조를 개선할 방법을 제안해줘"
```

### 명시적 사용

특정 파일의 코드 리뷰를 요청할 때:

```
code-style-reviewer Skill을 사용해서 @src/services/userService.ts를 분석해줘
```

## 📋 검사 항목

### 단일책임원칙 (SRP)
- 함수/메서드가 하나의 작업만 수행하는가?
- 클래스가 하나의 책임만 가지는가?
- 함수의 길이가 적절한가? (권장: 20줄 이하)

### DRY (Don't Repeat Yourself)
- 반복되는 코드 패턴이 있는가?
- 공통 로직이 추출될 수 있는가?
- 하드코딩된 설정 값이 있는가?

### 단순화 우선
- 불필요한 추상화가 있는가?
- 깊은 중첩 구조가 있는가? (권장: 3단계 이내)
- 과도하게 우아한(clever) 코드가 있는가?

### YAGNI (You Aren't Gonna Need It)
- 사용되지 않는 코드가 있는가?
- 미래를 대비한 불필요한 기능이 있는가?
- 죽은(dead) 코드가 있는가?

### 타입 안전성 (TypeScript)
- `any` 타입이 사용되었는가?
- 함수의 매개변수와 반환 타입이 정의되었는가?
- 인터페이스가 적절히 사용되었는가?

### 명명규칙
- 변수명이 명확하고 의미있는가?
- 함수명이 동사로 시작하는가?
- 일관성 있는 케이싱을 사용하는가?

## 📊 리뷰 리포트

리뷰 결과는 다음 형식으로 제공됩니다:

```
# Code Style Review Report

## 📄 파일: [filename]

### ✅ 좋은 점
- [좋은 사례들]

### ⚠️ Critical Issues
- [반드시 수정해야 할 문제들]

### 📢 Warnings
- [개선이 필요한 문제들]

### 💡 Suggestions
- [고려해볼 만한 제안들]

## 📊 종합 평가
- 전체 코드 품질 점수: [X/10]
- 가장 중요한 개선 사항: [상위 3개]
```

## 📚 상세 문서

플러그인에 포함된 문서:

- **SKILL.md** - Skill 정의 및 검사 프로세스
- **PRINCIPLES.md** - 각 원칙의 상세 설명과 체크리스트
- **EXAMPLES.md** - 나쁜 코드 vs 좋은 코드 예제

## 🔧 개발 및 테스트

### 로컬 테스트

```bash
# dev-marketplace 디렉토리로 이동
cd /Users/stefancho/works/claude-plugins/dev-marketplace

# Claude Code 시작
cd ..
claude

# Claude Code 내에서
/plugin marketplace add ./dev-marketplace
/plugin install code-style-plugin@dev-marketplace
```

### Skill 업데이트

`.claude/skills/code-style-reviewer/SKILL.md`를 수정한 후:

1. Claude Code 재시작
2. Skill 변경사항 적용 확인

## 🔄 팀과 공유

이 플러그인을 팀과 공유하려면:

1. 플러그인 디렉토리를 Git 저장소에 푸시
2. 팀원들이 다음 명령으로 설치:

```bash
/plugin install code-style-plugin@your-org/claude-plugins
```

## 📝 커스터마이징

각 원칙의 검사 기준을 프로젝트에 맞게 조정할 수 있습니다:

1. `SKILL.md`에서 검사 항목 수정
2. `PRINCIPLES.md`에서 상세 설명 업데이트
3. `EXAMPLES.md`에서 프로젝트 관련 예제 추가

## ⚖️ 라이선스

MIT License

## 👤 작성자

Stefan Cho

## 🤝 기여

개선 사항이나 버그 보고는 이슈 또는 PR을 통해 제출해주세요.

---

## 빠른 시작 체크리스트

- [ ] Plugin 설치
- [ ] 코드 리뷰 요청
- [ ] 리뷰 결과 확인
- [ ] 제안된 개선사항 적용
- [ ] 팀원들과 공유
