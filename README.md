# Web‑Based Collaborative Terminal via Cloudflare Tunnel

This repository provides a simple **web terminal** that runs on any VPS and can be exposed permanently through a **Cloudflare Tunnel**. It works similarly to **sshx.io**, letting you share a browser‑based terminal with anyone via a unique URL.

## How it works

1. **ttyd** (or **gotty**) runs a web server that serves a terminal over WebSockets.
2. **cloudflared** creates a tunnel from a sub‑domain of your Cloudflare‑managed domain to the local `ttyd` port.
3. The resulting public URL can be shared, and anyone can interact with the shell in real time.

## Features

- 🎯 Instant sharing – start the service and get a URL instantly.
- 🖥️ Browser‑based terminal – no SSH client required on the viewer side.
- 🔐 End‑to‑end encryption – Cloudflare terminates TLS; the tunnel is encrypted.
- 📡 Works behind NAT/firewalls – no inbound ports needed.
- 🛠️ Easy to run as a Docker container or a systemd service.

## Prerequisites

- A **Cloudflare account** with a zone (domain) added.
- **cloudflared** installed on the VPS (see Cloudflare docs).
- Docker installed (optional – you can also run `ttyd` directly).

## Quick start (Docker)

```bash
# 1. Install cloudflared (Debian/Ubuntu example)
curl -L https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb -o cloudflared.deb
sudo dpkg -i cloudflared.deb

# 2. Clone this repo and build the Docker image
git clone https://github.com/TrivCodez/sshx-collaborative-terminal.git
cd sshx-collaborative-terminal
docker build -t web-terminal .

# 3. Run the container (exposes ttyd on 7681 inside the container)
#    Replace <YOUR_TUNNEL_TOKEN> with the token you get from `cloudflared tunnel create`
cloudflared tunnel run --url http://localhost:7681 &

docker run -d --name web-terminal -p 7681:7681 web-terminal
```

After `cloudflared` starts, it will print a URL like `https://<random>.trycloudflare.com`. Share that URL – anyone opening it gets a full interactive shell.

## Running without Docker (direct binary)

```bash
# Install ttyd (Ubuntu example)
sudo apt-get install -y ttyd

# Start ttyd on port 7681
ttyd -p 7681 bash &

# Start the Cloudflare tunnel
cloudflared tunnel --url http://localhost:7681
```

## Systemd service (recommended for production)

Create `/etc/systemd/system/web-terminal.service`:

```ini
[Unit]
Description=Web terminal with ttyd and Cloudflare tunnel
After=network.target

[Service]
# Start ttyd
ExecStart=/usr/bin/ttyd -p 7681 bash
# Start cloudflared (replace <TOKEN> with your tunnel token)
ExecStartPost=/usr/local/bin/cloudflared tunnel --url http://localhost:7681
Restart=always
User=root
WorkingDirectory=/root

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now web-terminal.service
```

## Security considerations

- The terminal runs as the user you launch the service as – avoid running as root in production.
- Anyone with the URL can execute commands; treat the URL as a secret.
- Cloudflare terminates TLS, but the underlying `ttyd` connection is plain HTTP – the tunnel encrypts it.
- Use `cloudflared` access policies (Zero Trust) to restrict who can reach the tunnel if needed.

## License

MIT – see the `LICENSE` file.
