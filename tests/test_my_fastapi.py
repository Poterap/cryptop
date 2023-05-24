import datetime
import os
from fastapi.testclient import TestClient

from src.app.main import app
from src.parsers.D2.stooq_api import get_symbols
from src.config.config_reader import read_config
from src.utils.file_functions import create_folder_in_directory, create_full_file_path

config = read_config()

client = TestClient(app)

# python -m pytest tests/

def test_get_status():
    """
    Testuje czy endpoint /status zwraca status "ok" i poprawny format daty.
    """
    response = client.get("/status")
    assert response.status_code == 200
    assert response.json() == {"status": config['my_api']['status_message'], "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}


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
    test_symbol = config['pytest']['test_refresh_binance_data']['symbol']

    response = client.get(f"/refresh_binance/{test_symbol}")
    assert response.status_code == 200

    data = response.json()
    assert "message" in data
    assert "info" in data
    assert data["message"] == f"Data for {test_symbol} updated successfully"

    dir_path = create_folder_in_directory(name=config['binance_api']['creating_folder']['folder_for_saving_data_name'], path_directory=config['binance_api']['creating_folder']['folder_for_saving_data'], add_date=config['binance_api']['creating_folder']['folder_for_saving_data_is_with_date'])
    file_path = create_full_file_path(test_symbol, dir_path, True, ".csv")

    assert os.path.exists(file_path)


def test_refresh_stooq_data():
    """
    Testuje czy endpoint /refresh_stooq:
        - zwraca odpowiedni kod odpowiedzi
        - zwraca odpowiedznią wiadomość
        - sprawdza czy plik został pobrany i zapisany w odpowiednim miejscu
    """
    test_symbol = config['pytest']['test_refresh_stooq_data']['symbol']

    response = client.get(f"/refresh_stooq/{test_symbol}")
    assert response.status_code == 200

    data = response.json()
    assert "message" in data
    assert "info" in data
    assert data["message"] == f"Data for {test_symbol} updated successfully"

    dir_path = create_folder_in_directory(name=config['stooq_api']['creating_folder']['folder_for_saving_data_name'], path_directory=config['stooq_api']['creating_folder']['folder_for_saving_data'], add_date=config['stooq_api']['creating_folder']['folder_for_saving_data_is_with_date'])
    filepath = create_full_file_path(test_symbol, dir_path, True, ".csv")

    assert os.path.exists(filepath)







