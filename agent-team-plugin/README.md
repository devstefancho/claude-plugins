# agent-team-plugin

워크트리 세션에서 agent team을 생성, 확장, 정리하는 플러그인.

## 설치

```bash
/plugin marketplace add .
/plugin install agent-team-plugin@devstefancho-claude-plugins
```

## 커맨드 목록

| Command | Description |
|---------|-------------|
| `create team` (스킬) | planner + implementer 기본 팀 생성 |
| `/expand-team` | 기존 팀에 새 팀원 추가 |
| `/cleanup-team` | 팀원 종료 및 팀 정리 |

## 팀 생성

워크트리 세션에서 다음과 같이 트리거:

```
팀 생성해줘
create team
agent team 만들어줘
```

### 기본 팀 구성

| Member | Role |
|--------|------|
| team-lead | 오케스트레이션, 작업 할당 |
| planner | 브레인스톰, spec 작성 |
| implementer | 코드 구현, 테스트 작성 |

### 작업 흐름

```
Goal → planner(spec) → TaskCreate → team-lead review → implementer(code) → Done
```

## 팀 확장 (Expand)

기존 팀에 전문 역할 팀원을 추가:

```
/expand-team           # 역할 카탈로그에서 선택 (추천 포함)
/expand-team tester    # 직접 역할 지정
```

### 역할 카탈로그

| Role | Description | Best For |
|------|-------------|----------|
| **tester** | 테스트 작성, 커버리지 분석 | 구현 완료 후 품질 검증 |
| **reviewer** | 코드 리뷰, 보안/성능 체크 | PR 전 코드 품질 게이트 |
| **researcher** | 코드베이스 탐색, 기술 조사 | 새 기술 도입, 레거시 분석 |
| **architect** | 시스템 설계, API 설계 | 대규모 기능, 리팩토링 |
| **devops** | CI/CD, Docker, IaC | 인프라 작업, 파이프라인 |
| **ui-designer** | UI 컴포넌트, 디자인 시스템 | 프론트엔드 중심 작업 |
| **security-auditor** | 보안 취약점, CVE 검사 | 보안 감사, 릴리스 전 점검 |
| **custom** | 사용자 정의 역할 | 특수 작업 |

## 팀 정리 (Cleanup)

팀 작업이 완료되면 팀원을 종료:

```
/cleanup-team           # 팀원 목록 보여주고 선택
/cleanup-team --all     # 모든 팀원 종료 + 팀 삭제
/cleanup-team --unused  # 유휴 팀원만 종료
/cleanup-team --default # planner/implementer만 유지, 나머지 종료
```

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

팀 생성 시 자동으로 설정되는 항목:
- Planner: `/loop 10m /writing-specs update spec`
- Implementer: TaskList 주기적 확인
- 색상: 자동 할당 (프로그래밍 설정 불가)
