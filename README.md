# sshx Collaborative Terminal Wrapper

This repository provides a lightweight wrapper and usage guide for **[sshx.io](https://sshx.io)** – a secure, web‑based collaborative terminal. It enables you to share your command‑line environment instantly via a unique link, perfect for real‑time debugging, pair‑programming, teaching, or CI/CD debugging.

## Features

- **Instant sharing** – one command generates a sharable URL.
- **Real‑time collaboration** – multiple participants can type, see cursors, and chat.
- **End‑to‑end encryption** – the relay never sees your keystrokes.
- **Cross‑platform** – works on macOS, Linux, and Windows.
- **CI/CD integration** – can be used in GitHub Actions to debug failing workflows.

## Quick start (local machine)

```bash
# Install the sshx CLI (single‑line script)
curl -sSf https://sshx.io/get | sh

# Run sshx – a session will start and a link will be printed
sshx
```

Copy the printed link and share it with anyone you want to collaborate with.

## Using sshx in GitHub Actions (CI debugging)

Add a step to your workflow that installs sshx and starts a session when a job fails. Example:

```yaml
name: CI
on: [push, pull_request]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Build
        run: |
          # Your build commands here
          make test
      - name: Start sshx on failure
        if: failure()
        run: |
          curl -sSf https://sshx.io/get | sh
          sshx &
          echo "sshx session started – share the link above"
          # Keep the job alive for a short period to allow connection
          sleep 300
```

> **Note:** Keep the job alive only for a short time to avoid unnecessary charges. Remove the step when debugging is complete.

## Security considerations

- The session is **end‑to‑end encrypted**, but the relay server still hosts the connection metadata.
- Do not run privileged commands (e.g., `sudo`) inside a shared session unless you fully trust participants.
- Sessions are temporary; the link expires when you stop the sshx process.
- Treat the session like any public port exposure – avoid leaking secrets.

## License

MIT – see the `LICENSE` file.
