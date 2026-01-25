from fastapi.testclient import TestClient
from pomodoro_quest.main import app


def test_today_stats_endpoint():
    with TestClient(app) as client:
        res = client.get("/api/stats/today")
        assert res.status_code == 200
        body = res.json()
        assert "focus_sessions_completed" in body
        assert "break_sessions_completed" in body
        assert "total_completed_minutes" in body
