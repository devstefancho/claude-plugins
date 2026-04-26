# Git Commit Plugin

Git 변경사항을 분석하여 conventional commit 메시지를 자동으로 생성합니다.

## 기능

- **스마트 분석** - staged/unstaged 변경사항 자동 분석
- **스코프 감지** - 적절한 커밋 타입 결정 (feat, fix, chore 등)
- **사용자 확인** - 커밋 전 승인 요청
- **보안 검사** - 민감한 정보 포함 시 경고

## 설치

```bash
/plugin install git-commit-plugin@devstefancho-claude-plugins
```

## 사용법

```bash
/commit
```

이 커맨드는:
1. git 상태와 staged 변경사항 확인
2. 변경사항 분석
3. conventional commit 메시지 생성
4. 승인 요청
5. 커밋 실행

## 커밋 타입

- `feat`: 새로운 기능
- `fix`: 버그 수정
- `chore`: 유지보수 작업
- `docs`: 문서 변경
- `style`: 코드 포맷팅
- `refactor`: 코드 리팩토링
- `test`: 테스트 추가/수정
- `build`: 빌드 설정
- `ci`: CI/CD 변경

## 예시 출력

```
feat: Add user authentication feature
fix: Fix boundary value error in date range search
chore: Update dependency versions
```
