# python-monolit

Flask monolith — room reservation system (work in progress).

## Requirements

- Python 3.13+

## Local run

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements-dev.txt
cp .env.example .env
flask --app wsgi db upgrade
flask --app wsgi seed
flask --app wsgi run --debug --host 0.0.0.0 --port 5000
```

App: [http://localhost:5000](http://localhost:5000) — HTML shell with nav (Home / Book).

Health check:

```bash
curl -s http://localhost:5000/health
```

Expected response: `{"status":"ok"}`.

Readiness (database):

```bash
curl -s http://localhost:5000/ready
```

Expected response: `{"status":"ok"}` (HTTP 503 if the database is unreachable).

List rooms:

```bash
curl -s http://localhost:5000/api/rooms
```

Returns a JSON array (empty until rooms are seeded).

List / create reservations:

```bash
curl -s http://localhost:5000/api/reservations
curl -s -X POST http://localhost:5000/api/reservations \
  -H 'Content-Type: application/json' \
  -d '{"room_id":1,"guest_name":"Ada","guest_email":"ada@example.com","starts_at":"2026-08-01T10:00:00+00:00","ends_at":"2026-08-01T11:00:00+00:00"}'
```

Overlapping confirmed bookings for the same room return HTTP 409.

## Tests

```bash
pytest
```

Uses an in-memory SQLite database (`TestConfig`) — does not touch `instance/app.db`.

## Database migrations

Schema changes are managed with **Flask-Migrate** (Alembic). Models in `app/models.py` are the source of truth; migration scripts under `migrations/versions/` are generated from them and applied to the database.

On a fresh clone, apply existing migrations:

```bash
flask --app wsgi db upgrade
```

After changing models, create and apply a new migration:

```bash
flask --app wsgi db migrate -m "short description"
flask --app wsgi db upgrade
```

`db migrate` autogenerates a revision by comparing models to the current database — always review the generated file before upgrading.

## Database (SQLite)

Local development uses **SQLite** by default — no Docker or external database server required.

- Config: `DATABASE_URL=sqlite:///app.db` in [`.env.example`](.env.example)
- File on disk: `instance/app.db` (gitignored)
- Apply schema: `flask --app wsgi db upgrade`

Postgres via Docker can be added later; for now SQLite is enough.

## Configuration

Copy [`.env.example`](.env.example) to `.env` and edit values as needed. `.env` is gitignored; never commit real secrets.

`flask --app wsgi seed` creates an admin user (`ADMIN_USERNAME` / `ADMIN_PASSWORD`) and three sample rooms. Safe to re-run (skips existing rows).
