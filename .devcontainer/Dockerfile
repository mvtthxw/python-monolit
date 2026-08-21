FROM mcr.microsoft.com/devcontainers/base:jammy

ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=$USER_UID

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        sudo \
        curl \
        ca-certificates \
        git \
        docker.io \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /workspace
