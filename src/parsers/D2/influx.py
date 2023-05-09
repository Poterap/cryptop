import glob
import csv
import datetime
import sys
import os
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

# Database connection settings
token = "U2H9TCSHMNdtNaeyt7NwovtLIuKjC3LZRGCUSab6VgK3DWZSHBknt0IfZsCGXkJXWVMH2I8JurcXr0Jw0FWbLQ=="
org = "my-org"
bucket = "test"
url = "http://localhost:8086"

# Initialize InfluxDB client
client = InfluxDBClient(url=url, token=token)

# Path to the folder with CSV files
folder_path = './data/stooq_data_2023-05-04'

write_api = client.write_api(write_options=SYNCHRONOUS)

# Get the list of CSV files in the folder
try:
    files = glob.glob(f"{folder_path}/*.csv")
except Exception as e:
    print(f"Error getting list of CSV files: {e}")
    sys.exit()

for file_path in files:
    # Get the symbol and date from the file name
    try:
        file_name = os.path.basename(file_path)
        symbol, date_str = os.path.splitext(file_name)[0].split('_')
        date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
    except Exception as e:
        print(f"Error getting symbol and date from file name {file_name}: {e}")
        continue

    # Open the CSV file for the given stock

    with open(file_path) as csvfile:
        
        reader = csv.DictReader(csvfile)

        points = []

        rows_processed = 0
        rows_with_data = 0

        for row in reader:
            rows_processed += 1
            try:
                if row['Otwarcie'] and row['Najwyzszy'] and row['Najnizszy'] and row['Zamkniecie']:
                    rows_with_data += 1
                    volume_modified = False  # flag for volume modification
                    if row['Wolumen']:
                        volume_modified = True
                        volume = float(row['Wolumen'])
                    else:
                        volume_modified = False
                        volume = 0.0

                    point = (
                        Point(date)
                        .tag("symbol", symbol)
                        .time(row['Data'], WritePrecision.NS)
                        .field("open", float(row['Otwarcie']))
                        .field("high", float(row['Najwyzszy']))
                        .field("low", float(row['Najnizszy']))
                        .field("close", float(row['Zamkniecie']))
                        .field("volume", volume)
                    )
                    point.modified = {
                        "volume": volume_modified
                    }  # Add dictionery of flags to the point
                    points.append(point)
            except Exception as e:
                print(f"Error processing row {rows_processed} for {symbol} {row['Data']}: {e}")
                continue

    # Write all the points to the database
    try:
        write_api.write(bucket=bucket, org=org, record=points)
    except Exception as e:
        print(f"Error writing points to the database: {e}")
        continue

    print(f'{rows_processed} of {rows_with_data} rows processed for {symbol}')

