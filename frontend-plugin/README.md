# Frontend Plugin

React/Next.js 컴포넌트 설계 원칙 기반 코드 리뷰를 제공하는 Claude Code 플러그인입니다.

## 설치

```bash
/plugin install frontend-plugin@devstefancho-claude-plugins
```

## 포함된 Skills

### Component Design Reviewer

React/Next.js 컴포넌트의 설계 품질을 검사하는 Skill입니다.

**검사 원칙:**
- 단일 책임 원칙 (SRP)
- Props 설계 원칙 (Props drilling 탐지)
- 합성(Composition) 패턴
- 재사용성 원칙
- Custom Hooks 분리

**사용 예시:**
```
이 컴포넌트의 설계를 리뷰해주세요.
```

```
UserDashboard.tsx 파일의 컴포넌트 구조를 분석해주세요.
```

```
Props drilling 문제가 있는지 확인해주세요.
```

**자동 활성화 시나리오:**
- React/Next.js 컴포넌트 리뷰 요청
- 컴포넌트 구조 분석 요청
- Props 설계 검토 요청
- 컴포넌트 리팩토링 제안

## 관련 문서

- [SKILL.md](skills/component-design-reviewer/SKILL.md) - Skill 정의
- [PRINCIPLES.md](skills/component-design-reviewer/PRINCIPLES.md) - 원칙 상세 설명
- [EXAMPLES.md](skills/component-design-reviewer/EXAMPLES.md) - 코드 예시

## 버전

- 1.0.0: 초기 릴리스 - Component Design Reviewer Skill
