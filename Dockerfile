FROM python:3.13-slim-bookworm

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY requirements-prod.txt .
RUN pip install --no-cache-dir -r requirements-prod.txt

COPY wsgi.py entrypoint.sh ./
COPY migrations ./migrations
COPY app ./app

RUN chmod +x /app/entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["gunicorn", "-b", "0.0.0.0:8000", "wsgi:app"]
