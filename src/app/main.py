import datetime
import sys

from fastapi import FastAPI, HTTPException, Path
import requests

from src.log.logger import My_logger
from src.parsers.D2.stooq_api import get_symbols, download_stooq_data
from src.parsers.D1.binance_api import download_binance_data
from src.config.config_reader import read_config


config = read_config()

#Logger configuration
logger = My_logger(name=config['my_api']['logger_name'], filename=config['my_api']['logger_path'])

app = FastAPI()

@app.get("/status")
async def get_status():
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Received GET request for /status")
    return {"status": config['my_api']['status_message'], "timestamp": now}

@app.get("/symbols_stooq")
async def get_stooq_symbols():
    return {"symbols": get_symbols()}


@app.get("/refresh_binance/{crypto_symbol}")
async def refresh_binance_data(crypto_symbol: str = Path(..., description="Symbol of cryptocurrency to update eg. BTC or 'allc' for all cryptocurrencies")):
    """
    Updates data for a specific cryptocurrency or all cryptocurrencies from Binance.
    """
    try:
        info_list = []
        if crypto_symbol.lower() == "allc":
            cryptos = config['binance_api']['cryptos_symbols_for_binance_api']
            for crypto in cryptos:
                info = download_binance_data(crypto=crypto)
                info_list.append(info)
            message = "Data updated successfully for all cryptocurrencies"
            logger.info(message)
            return {"message": message, "info_list": info_list}
        else:
            info = download_binance_data(crypto=crypto_symbol)
            logger.info(f"Data for {crypto_symbol} updated successfully")
            return {"message": f"Data for {crypto_symbol} updated successfully", "info": info}
    except requests.exceptions.RequestException as e:
        logger.error(f"Error connecting to Binance API: {str(e)}")
        raise HTTPException(status_code=500, detail={"error": "Error connecting to Binance API", "details": str(e)})
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail={"error": str(e)})
    
@app.get("/refresh_stooq/{stock_symbol}")
async def refresh_stooq_data(stock_symbol):
    info_list = []
    if stock_symbol.lower() == "alls":
        for symbol_dict in config['stooq_api']['symbols']:
            for key in symbol_dict.keys():
                info = download_stooq_data(key)
                info_list.append(info)
        message = "Data updated successfully for all cryptocurrencies"
        logger.info(message)
        return {"message": message, "info_list": info_list}
    else:
        info = download_stooq_data(stock_symbol)
        logger.info(f"Data for {stock_symbol} updated successfully")
        return {"message": f"Data for {stock_symbol} updated successfully", "info": info}

