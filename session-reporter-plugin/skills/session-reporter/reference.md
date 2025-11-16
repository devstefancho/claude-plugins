# Session Reporter - Reference

## Overview

HTML 파일로 작업 세션을 시각화하여 브라우저에서 볼 수 있습니다.

## Trigger Keywords

**Korean**: "HTML로 보여줘", "HTML 파일로 만들어줘", "HTML로 저장"
**English**: "view as HTML", "export to HTML", "show in HTML"

## Report Scope Options

1. **마지막 작업만** - 최근 작업 내용만
2. **전체 세션** - 처음부터 모든 대화/변경사항
3. **커스텀 선택** - 원하는 내용만 선택

## File Location

```
/tmp/session-report-YYYYMMDD-HHMMSS.html
```

⚠️ `/tmp` 파일은 시스템 재시작시 삭제됩니다.

## Template Customization

템플릿 위치: `.claude/skills/session-reporter/templates/report.html`

### Placeholders

- `{{TITLE}}` - 리포트 제목
- `{{TIMESTAMP}}` - 생성 시간
- `{{SUMMARY}}` - 작업 요약
- `{{CONVERSATION}}` - 대화 내용
- `{{CHANGES}}` - 코드 변경사항
- `{{RESULTS}}` - 실행 결과
- `{{FILE_PATH}}` - 파일 경로

## Tips

- **공유 전 확인**: 민감한 정보(API 키, 비밀번호) 제거
- **영구 저장**: 중요한 리포트는 다른 위치에 복사
- **PDF 변환**: 브라우저의 인쇄 기능(Cmd+P) 사용
