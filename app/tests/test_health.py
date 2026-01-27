from fastapi.testclient import TestClient
from pomodoro_quest.main import app


def test_liveness_probe():
    with TestClient(app) as client:
        res = client.get("/api/health/live")
        assert res.status_code == 200
        assert res.json()["status"] == "alive"


def test_readiness_probe():
    with TestClient(app) as client:
        res = client.get("/api/health/ready")
        assert res.status_code == 200
        assert res.json()["status"] in ("ready", "not_ready")
