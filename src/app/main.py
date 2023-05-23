import datetime
import os
import sys

from fastapi import FastAPI, HTTPException, Path
from fastapi.responses import FileResponse
import requests

from src.log.logger import My_logger
from src.parsers.D2.stooq_api import download_all_stooq_data, get_symbols, download_stooq_data
from src.parsers.D1.binance_api import download_binance_data
from src.config.config_reader import read_config
import src.utils.file_functions as uti


config = read_config()

#Logger configuration
logger = My_logger(name=config['my_api']['logger_name'], filename=config['my_api']['logger_path'])

app = FastAPI()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:4200"  # angular
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/status")
async def get_status():
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"Received GET request for /status")
    return {"status": config['my_api']['status_message'], "timestamp": now}

@app.get("/symbols_stooq")
async def get_stooq_symbols():
    logger.info(f"Received GET request for /symbols_stooq")
    return {"symbols": get_symbols()}


@app.get("/refresh_binance/{crypto_symbol}")
async def refresh_binance_data(crypto_symbol: str = Path(..., description="Symbol of cryptocurrency to update eg. BTC or 'allc' for all cryptocurrencies")):
    """
    Updates data for a specific cryptocurrency or all cryptocurrencies from Binance. The symbol of the cryptocurrency represents the price in USDT.
    """
    try:
        info_list = []
        if crypto_symbol.lower() == "allc":
            info_list = download_all_stooq_data()
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
    try:
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
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        return {"message": f"An error occurred: {str(e)}"}

@app.get("/logs/{source}")
def get_logs(source: str = Path(..., description="Allowed values: 'my_api', 'scheduler', 'binance_api', 'stooq_api'.")):
    """
    Get logs file based on the source.
    """
    allowed_sources = config["my_api"]["sources_for_logs"]
    
    if source not in allowed_sources:
        raise HTTPException(status_code=400, detail="Invalid source provided")
    
    file_path = config[source]['logger_path']
    
    try:
        return FileResponse(file_path)
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Issue with the logs file")

@app.get("/available_eda_raports/{source}")
def get_folder_names(source: str):
    """
    Returns the names of folders in the specified directory based on the source.
    """
    allowed_sources = config["my_api"]["sources_for_data"]
    
    if source not in allowed_sources:
        raise HTTPException(status_code=400, detail="Invalid source provided")

    folder_path = config[f'{source}_api']['creating_folder']['folder_for_saving_data']

    datas = uti.get_datas_from_folder(folder_path)

    folder_names = {}
    for date in datas:
        folder_date_path = os.path.join(folder_path, f"stooq_data_{date}")
        try:
            raports = uti.get_files_from_folder(os.path.join(folder_date_path, "automatic_eda"))
        except ValueError:
            datas.remove(date)
            continue
        folder_names[date] = raports

    return {"datas": folder_names}

@app.get("/data/{symbol}/{date}/{source}")
def get_data(symbol: str, date: str, source: str):
    """
    Returns the eda raport for the specified symbol, date and source.
    """

    allowed_sources = config["my_api"]["sources_for_data"]
    
    if source not in allowed_sources:
        raise HTTPException(status_code=400, detail="Invalid source provided")

    file_path = config[f'{source}_api']['creating_folder']['folder_for_saving_data']
    file_path = os.path.join(file_path, f"stooq_data_{date}")
    file_path = os.path.join(file_path, "automatic_eda")
    file_name = f"{symbol}_{date}_report.html"
    file_path = os.path.join(file_path, file_name)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Report not found.")

    return FileResponse(file_path, filename=file_name)
