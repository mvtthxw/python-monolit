"""API smoke tests for health, readiness, and reservations."""

from flask.testing import FlaskClient

from app.models import Room


def test_health(client: FlaskClient) -> None:
    """Liveness endpoint returns ok."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}


def test_ready(client: FlaskClient) -> None:
    """Readiness endpoint succeeds when the database is available."""
    response = client.get("/ready")
    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}


def test_create_reservation(client: FlaskClient, room: Room) -> None:
    """POST /api/reservations creates a confirmed booking."""
    response = client.post(
        "/api/reservations",
        json={
            "room_id": room.id,
            "guest_name": "Ada",
            "guest_email": "ada@example.com",
            "starts_at": "2026-10-01T10:00:00+00:00",
            "ends_at": "2026-10-01T11:00:00+00:00",
        },
    )
    assert response.status_code == 201
    body = response.get_json()
    assert body is not None
    assert body["room_id"] == room.id
    assert body["guest_name"] == "Ada"
    assert body["status"] == "confirmed"


def test_create_reservation_conflict(client: FlaskClient, room: Room) -> None:
    """Overlapping confirmed reservations on the same room return 409."""
    payload = {
        "room_id": room.id,
        "guest_name": "Ada",
        "guest_email": "ada@example.com",
        "starts_at": "2026-10-02T10:00:00+00:00",
        "ends_at": "2026-10-02T12:00:00+00:00",
    }
    first = client.post("/api/reservations", json=payload)
    assert first.status_code == 201

    conflict = client.post(
        "/api/reservations",
        json={
            **payload,
            "guest_name": "Bob",
            "guest_email": "bob@example.com",
            "starts_at": "2026-10-02T11:00:00+00:00",
            "ends_at": "2026-10-02T13:00:00+00:00",
        },
    )
    assert conflict.status_code == 409
    assert conflict.get_json() == {"error": "reservation conflict"}
