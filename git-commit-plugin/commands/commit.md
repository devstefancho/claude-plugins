---
description: 변경사항을 분석하여 conventional commit 형식으로 자동 커밋
allowed-tools: Bash(git status:*), Bash(git diff:*), Bash(git add:*), Bash(git commit:*), Bash(git log:*)
---

# Git Commit 자동 생성

변경된 파일과 내용을 분석하여 적절한 conventional commit 메시지를 자동으로 생성하고 커밋합니다.

<context>
현재 git 상태를 확인합니다:

!`git status`: 현재 변경사항 및 staging 상태 확인
!`git diff --cached`: staged된 변경사항 상세 확인 (staged 파일이 없으면 unstaged 파일도 확인)
!`git log -5 --oneline --no-decorate`: 최근 커밋 메시지 스타일 참고
</context>

<instruction>
다음 단계를 수행합니다:

1. **변경사항 분석**
   - staged된 파일이 없으면 사용자에게 알리고 어떤 파일을 stage할지 제안
   - 변경된 파일 경로와 내용을 분석
   - 프로젝트 구조를 고려하여 적절한 스코프 결정

2. **커밋 스코프 자동 결정**
   다음 규칙으로 스코프를 선택:
   - `feat`: 새로운 기능, 컴포넌트, API 엔드포인트, UI 추가
   - `fix`: 버그 수정, 에러 핸들링, 오류 수정
   - `chore`: 의존성 업데이트, 설정 파일 변경, 빌드 설정
   - `docs`: README, 문서 파일 (*.md), 주석 변경
   - `style`: 코드 포맷팅, CSS, 스타일 수정 (기능 변경 없음)
   - `refactor`: 기능 변경 없는 코드 구조 개선, 리팩토링
   - `test`: 테스트 코드 추가/수정, 테스트 설정
   - `build`: 빌드 스크립트, 패키지 설정 변경
   - `ci`: CI/CD 설정 변경

3. **커밋 메시지 작성** (한국어)
   - 형식: `{scope}: {명확하고 간결한 한국어 요약}`
   - 요약은 동사로 시작 (예: "추가", "수정", "개선", "제거")
   - 50자 이내로 작성
   - 필요시 빈 줄 후 상세 설명 추가 (각 줄 72자 이내)

4. **사용자 확인 요청**
   - 생성된 커밋 메시지 보여주기
   - 주요 변경사항 요약 (diff 하이라이트)
   - AskUserQuestion 도구를 사용하여 승인 또는 수정 요청
   - 옵션: "커밋 실행", "메시지 수정", "취소"

5. **커밋 실행**
   - 승인되면: `git commit -m "생성된 메시지"`
   - 수정 요청되면: 사용자 피드백 반영하여 메시지 재작성 후 다시 확인
   - 취소되면: 작업 중단
</instruction>

<important>
- staged된 변경사항이 없으면 먼저 `git add` 할 파일을 제안합니다
- 여러 스코프에 해당하는 변경사항이 섞여있으면 가장 주요한 것을 선택하거나 분리 커밋을 제안합니다
- 민감한 정보(API 키, 비밀번호 등)가 포함된 파일은 경고합니다
- 커밋 메시지는 프로젝트의 최근 커밋 스타일을 참고하여 일관성을 유지합니다
- 빈 커밋은 생성하지 않습니다
</important>

<examples>
좋은 커밋 메시지 예시:
- `feat: 사용자 인증 기능 추가`
- `fix: 날짜 범위 검색 시 경계값 오류 수정`
- `chore: 의존성 버전 업데이트`
- `docs: API 사용 예제 추가`
- `refactor: 서비스 레이어 코드 구조 개선`
- `test: 단위 테스트 추가`
</examples>
