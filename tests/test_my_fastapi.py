import datetime
from fastapi.testclient import TestClient

from src.app.main import app
from src.parsers.D2.stooq_api import get_symbols

client = TestClient(app)

# python -m pytest tests/

def test_get_status():
    """
    Testuje czy endpoint /status zwraca status "ok" i poprawny format daty.
    """
    response = client.get("/status")
    assert response.status_code == 200
    assert response.json() == {"status": "okey", "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

def test_get_symbols_stooq():
    """
    Testuje czy endpoint /status zwraca poprawnie symbole
    """
    response = client.get("/symbols_stooq")
    assert response.status_code == 200

    endpoint_symbols = response.json()["symbols"]
    all_symbols = get_symbols()

    assert endpoint_symbols == all_symbols

def test_refresh_binance_data():
    """
    Testuje czy endpoint /refresh_binance
    """

    test_crypto_symbol = "BTC"

    response = client.get(f"/refresh_binance/{test_crypto_symbol}")
    assert response.status_code == 200

    data = response.json()
    assert "message" in data
    assert "info" in data
    assert data["message"] == f"Data for {test_crypto_symbol} updated successfully"





