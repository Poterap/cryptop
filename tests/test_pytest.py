import datetime
from fastapi.testclient import TestClient

from src.app.main import app

client = TestClient(app)

def test_get_status():
    """
    Testuje czy endpoint /status zwraca status "ok" i poprawny format daty.
    """
    response = client.get("/status")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
