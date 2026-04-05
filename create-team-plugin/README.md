# create-team-plugin

워크트리 세션에서 planner + implementer agent team을 자동 생성하는 스킬 플러그인.

## 설치

```bash
/plugin marketplace add .
/plugin install create-team-plugin@devstefancho-claude-plugins
```

## 사용법

워크트리 세션에서 다음과 같이 트리거:

```
팀 생성해줘
create team
agent team 만들어줘
```

## 팀 구성

| Member | Role | Color |
|--------|------|-------|
| team-lead | 오케스트레이션, 작업 할당 | - |
| planner | 브레인스톰, spec 작성 | auto-assigned |
| implementer | 코드 구현, 테스트 작성 | auto-assigned |

## 작업 흐름

```
Goal → planner(spec) → TaskCreate → team-lead review → implementer(code) → Done
```

1. team-lead에게 목표를 설명
2. planner가 `specs/` 디렉토리에 spec 작성
3. planner가 구현 태스크 생성 (TaskCreate)
4. team-lead가 리뷰 후 implementer에게 할당
5. implementer가 spec 기반으로 코드 + 테스트 작성

## 전제 조건

- `claude -w`로 워크트리 세션 시작 필요
- `writing-specs-plugin` 설치 권장 (planner의 spec 작성에 활용)

## Teammate 1M Context 설정

Teammate는 기본적으로 표준 Opus 모델(1M 아님)을 사용합니다. 1M context를 사용하려면:

```bash
export ANTHROPIC_DEFAULT_OPUS_MODEL='claude-opus-4-6[1m]'
```

`.zshrc`에 추가하면 영구 적용됩니다.

## 자동 설정

스킬 실행 시 자동으로 설정되는 항목:
- Planner: `/loop 10m /writing-specs update spec`
- Implementer: TaskList 주기적 확인
- 색상: 자동 할당 (프로그래밍 설정 불가)
