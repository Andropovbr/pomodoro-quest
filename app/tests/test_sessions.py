from fastapi.testclient import TestClient
from pomodoro_quest.main import app


def test_session_start_and_complete():
    client = TestClient(app)

    start_res = client.post("/api/sessions/start", json={"mode": "focus", "planned_minutes": 25})
    assert start_res.status_code == 200
    session_id = start_res.json()["session_id"]

    complete_res = client.post("/api/sessions/complete", json={"session_id": session_id, "completed_minutes": 25})
    assert complete_res.status_code == 200
    body = complete_res.json()
    assert body["session_id"] == session_id
    assert body["status"] == "completed"
    assert body["xp_gained"] == 10
