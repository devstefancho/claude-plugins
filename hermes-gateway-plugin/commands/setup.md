---
description: Hermes Agent 연결 설정 및 상태 확인 (로컬/SSH 모드 전환 지원)
argument-hint: "[--mode auto|local|ssh] [--remote-host <host>] [--remote-port <port>] [--local-port <port>] [--api-key <key>]"
allowed-tools: Bash(node:*), AskUserQuestion
---

Hermes 연결을 설정하고 상태를 확인한다.

## 인자가 없는 경우

연결 상태만 확인:
```bash
node "${CLAUDE_PLUGIN_ROOT}/scripts/hermes-companion.mjs" setup
```

## 인자가 있는 경우

config를 업데이트하고 연결 확인:
```bash
node "${CLAUDE_PLUGIN_ROOT}/scripts/hermes-companion.mjs" setup $ARGUMENTS
```

## 사용자가 설정 변경을 요청하지만 구체적 값이 없는 경우

AskUserQuestion으로 물어본다:
- "어떤 모드로 변경할까요?" → choices: auto, local, ssh
- SSH 모드 선택 시: "SSH 호스트 이름은?" (기본값: arch)

## 사용 가능한 플래그

- `--mode auto|local|ssh` — 연결 모드 변경
- `--remote-host <host>` — SSH 원격 호스트 (기본: arch)
- `--remote-port <port>` — 원격 Hermes 포트 (기본: 8642)
- `--local-port <port>` — SSH 터널 로컬 포트 (기본: 18642)
- `--api-key <key>` — Hermes API 키 설정

## 예시

- `/hermes:setup` → 현재 연결 상태 확인
- `/hermes:setup --mode ssh` → SSH 모드로 전환
- `/hermes:setup --mode ssh --remote-host myserver` → SSH 모드 + 호스트 변경
- `/hermes:setup --mode local` → 로컬 모드로 전환
- `/hermes:setup --mode auto` → 자동 감지 모드

Config 파일 위치: `~/.claude/hermes/config.json`
