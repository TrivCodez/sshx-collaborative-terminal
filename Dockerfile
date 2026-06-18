# Use a small Debian image with ttyd and cloudflared
FROM debian:bookworm-slim

# Install dependencies
RUN apt-get update && apt-get install -y \ 
    ca-certificates \ 
    curl \ 
    git \ 
    ttyd \ 
    && rm -rf /var/lib/apt/lists/*

# Install cloudflared (latest)
RUN curl -L https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb -o cloudflared.deb \
    && dpkg -i cloudflared.deb \
    && rm cloudflared.deb

# Expose the ttyd port
EXPOSE 7681

# Default command runs ttyd serving bash
CMD ["ttyd", "-p", "7681", "bash"]
