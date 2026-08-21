FROM mcr.microsoft.com/devcontainers/base:jammy

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        sudo \
        curl \
        ca-certificates \
        git \
        docker.io \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /workspace
