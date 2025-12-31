# Session Reporter Plugin

Claude Code 작업 세션을 시각화하는 HTML 리포트를 생성합니다.

## 기능

- **세션 시각화** - 대화 기록, 코드 변경, 실행 결과 확인
- **유연한 범위** - 마지막 작업만 또는 전체 세션 내보내기
- **자동 열기** - HTML 파일이 브라우저에서 자동으로 열림
- **깔끔한 포맷** - 구문 강조 및 섹션 탐색

## 설치

```bash
/plugin install session-reporter-plugin@devstefancho-claude-plugins
```

## 사용법

다음과 같이 HTML로 보기를 요청하면 스킬이 호출됩니다:

- "HTML로 보여줘"
- "HTML 파일로 만들어줘"
- "view as HTML"
- "export to HTML"

## 리포트 내용

- **작업 요약** - 수정된 파일, 주요 결정, 주요 변경사항
- **대화** - 사용자 질문과 Claude 응답
- **코드 변경** - 변경 전후 비교
- **실행 결과** - 테스트 결과, 빌드 출력, 에러

## 출력

리포트는 `/tmp/session-report-{timestamp}.html`에 저장됩니다
