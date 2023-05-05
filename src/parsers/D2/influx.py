import os
import csv
import datetime
import sys
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

# Ustawienia połączenia z bazą danych
token = "U2H9TCSHMNdtNaeyt7NwovtLIuKjC3LZRGCUSab6VgK3DWZSHBknt0IfZsCGXkJXWVMH2I8JurcXr0Jw0FWbLQ=="
org = "my-org"
bucket = "stooq"
url = "http://localhost:8086"

# Inicjalizacja klienta bazy danych
client = InfluxDBClient(url=url, token=token)

# Ścieżka do folderu z plikami CSV
folder_path = './data/stooq_data_2023-05-04'

write_api = client.write_api(write_options=SYNCHRONOUS)

# Pobranie listy plików z danego folderu
for file_name in os.listdir(folder_path):
    # Pobranie symbolu i daty z nazwy pliku
    symbol, date_str = os.path.splitext(file_name)[0].split('_')
    date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()

    file_path = os.path.join(folder_path, file_name)

    # Otwarcie pliku CSV dla danej spółki
    with open(file_path) as csvfile:
        reader = csv.DictReader(csvfile)

        count = 0
        rcount = 0

        for row in reader:
            count += 1
            try:
                if row['Otwarcie'] and row['Najwyzszy'] and row['Najnizszy'] and row['Zamkniecie']:
                    rcount += 1
                    point = (
                        Point(date)
                        .tag("symbol", symbol)
                        .time(row['Data'], WritePrecision.NS)
                        .field("open", float(row['Otwarcie']))
                        .field("high", float(row['Najwyzszy']))
                        .field("low", float(row['Najnizszy']))
                        .field("close", float(row['Zamkniecie']))
                        .field("volume", float(row['Wolumen']) if row['Wolumen'] else 0.0)
                    )

                write_api.write(bucket=bucket, org=org, record=point)
            except Exception as e:
                print(f"Błąd dla wiersza {count} {symbol} {row['Data']}: {e}")

        print(f'{count} of {rcount} rows processed for {symbol}')