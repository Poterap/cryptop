import datetime
import logging
import sys
import uvicorn

from fastapi import FastAPI, HTTPException, Path
import requests

# sys.path.append("..")

# from parsers.D2.test import return_okay
# from parsers.D1.binance_api import download_binance_data


# logging.basicConfig(
#     format='{"timestamp":"%(asctime)s", "level":"%(levelname)s", "function":"%(funcName)s", "message":"%(message)s"}',
#     level=logging.INFO,
#     handlers=[
#         logging.FileHandler("../../log/api.log"),
#         logging.StreamHandler()
#     ]
# )

app = FastAPI()

@app.get("/status")
async def get_status():
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logging.info(f"Received GET request for /status")
    return {"status": "ok", "timestamp": now}

# @app.get("/update_binance/{crypto_symbol}")
# async def update_data(crypto_symbol: str = Path(..., description="Symbol of cryptocurrency to update eg. BTC or 'allc' for all cryptocurrencies")):
#     """
#     Updates data for a specific cryptocurrency or all cryptocurrencies from Binance.
#     """
#     try:
#         info_list = []
#         if crypto_symbol.lower() == "allc":
#             cryptos = ['BTC', 'ETH', 'XRP', 'ADA', 'SOL', 'DOT', 'LTC', 'TRX', 'DAI', 'UNI', 'ETC', 'XLM', 'XMR', 'BCH', 'FIL', 'APT', 'VET', 'APE', 'ICP', 'GRT', 'FTM', 'EOS', 'MKR']
#             for crypto in cryptos:
#                 info = download_binance_data(crypto=crypto)
#                 info_list.append(info)
#             message = "Data updated successfully for all cryptocurrencies"
#             logging.info(message)
#             return {"message": message, "info_list": info_list}
#         else:
#             info = download_binance_data(crypto=crypto_symbol)
#             logging.info(f"Data for {crypto_symbol} updated successfully")
#             return {"message": f"Data for {crypto_symbol} updated successfully", "info": info}
#     except requests.exceptions.RequestException as e:
#         logging.error(f"Error connecting to Binance API: {str(e)}")
#         raise HTTPException(status_code=500, detail={"error": "Error connecting to Binance API", "details": str(e)})
#     except Exception as e:
#         logging.error(f"Error: {str(e)}")
#         raise HTTPException(status_code=500, detail={"error": str(e)})

