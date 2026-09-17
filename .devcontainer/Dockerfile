FROM mcr.microsoft.com/devcontainers/python:1-3.13-bookworm

# Zusätzliche Laufzeiten kommen über Dev Container Features.
COPY scripts/requirements.txt /tmp/template-requirements.txt
RUN python -m venv /opt/template-tools \
    && /opt/template-tools/bin/pip install --no-cache-dir \
       -r /tmp/template-requirements.txt specify-cli==1.0.7 \
    && chown -R vscode:vscode /opt/template-tools
ENV PATH="/opt/template-tools/bin:${PATH}"
