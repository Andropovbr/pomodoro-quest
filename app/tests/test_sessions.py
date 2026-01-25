from fastapi.testclient import TestClient
from pomodoro_quest.main import app


def test_session_start_complete_and_xp_accumulates():
    with TestClient(app) as client:
        me1 = client.get("/api/me")
        assert me1.status_code == 200
        xp_before = me1.json()["xp"]

        start_res = client.post("/api/sessions/start", json={"mode": "focus", "planned_minutes": 25})
        assert start_res.status_code == 200
        session_id = start_res.json()["session_id"]

        complete_res = client.post("/api/sessions/complete", json={"session_id": session_id, "completed_minutes": 25})
        assert complete_res.status_code == 200
        body = complete_res.json()
        assert body["xp_gained"] == 10

        me2 = client.get("/api/me")
        assert me2.status_code == 200
        assert me2.json()["xp"] == xp_before + 10
