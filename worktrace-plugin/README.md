# Worktrace Plugin

Claude Code 작업 히스토리를 추출하여 프로젝트/티켓별로 그룹화된 일일 요약을 생성합니다.

## Features

- `~/.claude/history.jsonl`에서 작업 히스토리 추출
- 티켓 번호 및 프로젝트별 자동 그룹화
- 마크다운 또는 JSON 출력 지원
- 기존 데일리 파일 업데이트 시 다른 섹션 보존
- 타임존 지원

## Installation

```bash
/plugin install worktrace-plugin@devstefancho-claude-plugins
```

## Usage

### Slash Command

```
/trace
```

이 커맨드는 worktrace 스킬을 호출하여 오늘의 작업 히스토리를 추출하고 데일리 노트를 업데이트합니다.

### Direct Script Usage

```bash
# 기본 사용 (stdout 출력)
python scripts/worktrace.py

# 특정 디렉토리에 저장
python scripts/worktrace.py --output-dir ./daily

# 커스텀 티켓 패턴
python scripts/worktrace.py --ticket-pattern "AMAP-\d+" --ticket-pattern "IE-\d+"

# 특정 날짜 및 타임존
python scripts/worktrace.py --date 2024-12-31 --timezone Asia/Seoul

# 설정 파일 사용
python scripts/worktrace.py --config config.json

# JSON 출력
python scripts/worktrace.py --json
```

## Configuration

`config.example.json`을 `config.json`으로 복사하여 설정:

```json
{
  "history_file": "~/.claude/history.jsonl",
  "output_dir": "./daily",
  "ticket_patterns": ["[A-Z]+-\\d+"],
  "timezone": "Asia/Seoul",
  "section_title": "## Claude Code Work History"
}
```

**우선순위**: CLI args > config.json > defaults

## Output Example

```markdown
## Claude Code Work History

### PROJ-123 (webapp)
- **Directory**: `/Users/user/projects/webapp/feat/PROJ-123`
- **Session**: `464c991b-f368-4ac4-9376-4fe6f1c9147e`
- Implement login form validation
- Fix password reset flow

### API-456 (api-service)
- **Directory**: `/Users/user/projects/api-service/bugfix/API-456`
- **Session**: `abc12345-...`
- Fix null pointer exception in user service

### Other (docs)
- **Directory**: `/Users/user/projects/docs`
- **Session**: `xyz78910-...`
- Update README documentation
```

## File Handling

`--output-dir` 지정 시:
- `{YYYY-MM-DD}.md` 파일 생성
- 파일이 이미 존재하면 `## Claude Code Work History` 섹션만 교체
- 다른 섹션은 보존됨

## Development

플러그인 테스트:

```bash
# 마켓플레이스 추가
/plugin marketplace add .

# 플러그인 설치
/plugin install worktrace-plugin@devstefancho-claude-plugins

# Claude Code 재시작 후 사용
/trace
```

## See Also

- [SKILL.md](skills/worktrace/SKILL.md) - 스킬 정의
- [template.md](skills/worktrace/references/template.md) - 템플릿 참조
- [summarize.md](skills/worktrace/references/summarize.md) - 요약 가이드라인
