# Cloudflare SSH Tunnel

A lightweight Python tool that runs on a VPS to expose a permanent **SSH** service via a Cloudflare Tunnel (cloudflared).  
It behaves like **sshx** but stays up continuously, automatically reconnecting if the tunnel drops.

## Features

- 📡 Persistent Cloudflare Tunnel exposing SSH (port 22)
- 🔄 Automatic restart on failure
- 🛡️ Works behind NAT / firewall without opening ports
- 🐍 Pure Python wrapper around `cloudflared`
- 📦 Minimal dependencies (standard library only)

## Prerequisites

- A VPS with **Python 3.8+** installed
- A **Cloudflare account** with a zone (domain) added
- The **cloudflared** binary installed on the VPS (see Cloudflare docs)

## Quick start

```bash
# 1. Install cloudflared (example for Debian/Ubuntu)
curl -L https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb -o cloudflared.deb
sudo dpkg -i cloudflared.deb

# 2. Clone the repository
git clone https://github.com/TrivCodez/sshx-collaborative-terminal.git
cd sshx-collaborative-terminal

# 3. Run the tunnel (you may want to run it as a service)
python3 -m src.main
```

The script will launch `cloudflared` with the arguments `tunnel --url ssh://localhost:22` and keep it running forever. If the process exits, it will automatically restart after a short delay.

## Running as a systemd service (recommended)

```ini
# /etc/systemd/system/cloudflare-ssh-tunnel.service
[Unit]
Description=Persistent Cloudflare SSH Tunnel
After=network.target

[Service]
ExecStart=/usr/bin/python3 -m src.main
Restart=always
RestartSec=5
User=root
WorkingDirectory=/path/to/sshx-collaborative-terminal

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now cloudflare-ssh-tunnel
```

## License

MIT License – see the `LICENSE` file.
