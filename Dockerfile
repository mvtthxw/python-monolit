FROM python:3.13-alpine@sha256:7984cf56ceaddebe4fefeb75d64000b9f45d8b77b11a09b24524da6cdc3af0c8 AS build

ENV PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PYTHONDONTWRITEBYTECODE=1

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

WORKDIR /app

COPY requirements-prod.txt .
RUN pip install --no-cache-dir -r requirements-prod.txt \
    && pip uninstall -y pip \
    && find /opt/venv -type d -name '__pycache__' -prune -exec rm -rf '{}' +

FROM python:3.13-alpine@sha256:7984cf56ceaddebe4fefeb75d64000b9f45d8b77b11a09b24524da6cdc3af0c8

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/venv/bin:$PATH"

WORKDIR /app

RUN addgroup -g 1010 app \
    && adduser -D -H -u 1010 -G app -s /sbin/nologin app

COPY --from=build /opt/venv /opt/venv
COPY --chown=app:app wsgi.py entrypoint.sh ./
COPY --chown=app:app migrations ./migrations
COPY --chown=app:app app ./app

RUN chmod 555 /app/entrypoint.sh

USER 1010

EXPOSE 8000

ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["gunicorn", "-b", "0.0.0.0:8000", "wsgi:app"]
