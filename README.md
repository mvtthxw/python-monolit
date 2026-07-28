# python-monolit

Flask monolith — room reservation system (work in progress).

## Requirements

- Python 3.13+

## Local run

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements-dev.txt
flask --app wsgi run --debug --host 0.0.0.0 --port 5000
```

App: [http://localhost:5000](http://localhost:5000)

Health check:

```bash
curl -s http://localhost:5000/health
```

Expected response: `{"status":"ok"}`.
