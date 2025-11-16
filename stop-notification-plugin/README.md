# Stop Notification Plugin

Claude Code 작업 완료 시 macOS 알림을 표시하는 플러그인입니다.

## 기능

- Claude가 응답을 완료할 때마다 macOS 네이티브 다이얼로그 알림 표시
- 3초 후 자동으로 닫힘
- 한국어 메시지 지원

## 요구사항

- macOS (osascript 사용)
- Claude Code

## 설치

```bash
/plugin install stop-notification-plugin@devstefancho-claude-plugins
```

설치 후 Claude Code를 재시작하면 활성화됩니다.

## 제거

```bash
/plugin uninstall stop-notification-plugin@devstefancho-claude-plugins
```

## 동작 방식

이 플러그인은 Claude Code의 `Stop` 이벤트 hook을 사용합니다. Claude가 응답을 완료할 때마다 다음과 같은 알림이 표시됩니다:

- **제목:** Claude Code 작업 완료
- **메시지:** Claude가 작업을 완료했습니다
- **버튼:** 확인
- **자동 닫힘:** 3초

## 커스터마이징

알림 메시지나 동작을 변경하려면 `hooks/stop-notification.sh` 스크립트를 수정하세요.

## 라이선스

MIT
