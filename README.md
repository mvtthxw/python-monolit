# python-monolit

Flask monolith — room reservation system (work in progress).

## Requirements

- Python 3.13+

## Local run

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements-dev.txt
flask --app wsgi db upgrade
flask --app wsgi run --debug --host 0.0.0.0 --port 5000
```

App: [http://localhost:5000](http://localhost:5000)

Health check:

```bash
curl -s http://localhost:5000/health
```

Expected response: `{"status":"ok"}`.

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

Default local database is SQLite (`instance/app.db`, gitignored). Override with `DATABASE_URL` if needed.
