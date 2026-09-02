# Secrets

Do not read, print, or copy secret values. Existence and field names are enough.

Typical locations (not exhaustive): `~/.secrets/`, `~/.ssh/`, `~/.aws/`, `~/.kube/`, `~/.netrc`, `.env`, `.env.*`, `*.pem`, `*_rsa`.

If a value must be used, tell the user to put it in a file under `~/.secrets/` (mode 0600) and have a script read it there. Do not ask them to paste it into the chat or a command line.
