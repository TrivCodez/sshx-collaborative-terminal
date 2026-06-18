#!/usr/bin/env python3
"""
cloudflare_ssh_tunnel.py

A simple wrapper that runs a Cloudflare tunnel exposing SSH (port 22) on the local
machine and keeps it alive forever. It is meant to be run on a VPS behind a
firewall/NAT, providing permanent SSH access without opening inbound ports.

Usage:
    python -m src.main
"""

import subprocess
import time
import sys
import signal

CLOUDFLARED_CMD = [
    "cloudflared",
    "tunnel",
    "--url",
    "ssh://localhost:22",
    "--no-autoupdate",
]

def run_tunnel():
    """Start the cloudflared process and restart it if it exits."""
    while True:
        try:
            proc = subprocess.Popen(CLOUDFLARED_CMD)
            # Forward termination signals to the child process.
            def _handle_sig(signum, frame):
                proc.terminate()
            for sig in (signal.SIGINT, signal.SIGTERM):
                signal.signal(sig, _handle_sig)

            proc.wait()
        except Exception as exc:
            print(f"[cloudflare-ssh-tunnel] error: {exc}", file=sys.stderr)

        print("[cloudflare-ssh-tunnel] tunnel stopped, restarting in 5s...", flush=True)
        time.sleep(5)

if __name__ == "__main__":
    run_tunnel()
