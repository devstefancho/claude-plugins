# Stop Notification Plugin

Display macOS notifications when Claude Code finishes working.

## Features

- Display macOS native dialog notification when Claude completes a response
- Auto-closes after 3 seconds
- Customizable message

## Requirements

- macOS (uses osascript)
- Claude Code

## Installation

```bash
/plugin install stop-notification-plugin@devstefancho-claude-plugins
```

Restart Claude Code after installation to activate.

## Uninstall

```bash
/plugin uninstall stop-notification-plugin@devstefancho-claude-plugins
```

## How It Works

This plugin uses Claude Code's `Stop` event hook. Each time Claude completes a response, a notification is displayed:

- **Title:** Claude Code Task Complete
- **Message:** Claude has finished working
- **Button:** OK
- **Auto-close:** 3 seconds

## Customization

To change the notification message or behavior, modify the `hooks/stop-notification.sh` script.

## License

MIT
