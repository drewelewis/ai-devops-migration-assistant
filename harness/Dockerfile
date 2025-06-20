# Harness Docker Runner 
FROM debian:bookworm-slim

# Install Docker CLI and other needed utilities
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        ca-certificates \
        curl \
        gnupg \
        lsb-release && \
    # Install Docker's official GPG key and CLI
    curl -fsSL https://download.docker.com/linux/debian/gpg | gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg && \
    echo \
      "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/debian \
      $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null && \
    apt-get update && \
    apt-get install -y --no-install-recommends docker-ce-cli && \
    rm -rf /var/lib/apt/lists/*

# Copy and set up the binary
COPY harness-docker-runner-linux-amd64 /usr/local/bin/harness-docker-runner
RUN chmod +x /usr/local/bin/harness-docker-runner

EXPOSE 3000
CMD ["harness-docker-runner", "server"]

