import app as module


def test_health():
    response = module.app.test_client().get("/health")
    assert response.status_code == 200
    assert response.get_json() == {"status": "alive"}


def test_ready_reports_dependency_failure(monkeypatch):
    class BrokenRedis:
        def ping(self):
            raise ConnectionError("expected test failure")

    monkeypatch.setattr(module, "redis_client", lambda: BrokenRedis())
    response = module.app.test_client().get("/ready")
    assert response.status_code == 503
    assert response.get_json()["status"] == "not-ready"

