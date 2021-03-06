#import talib
import numpy as np
import pickle
from pathlib import Path
import quandl
import os
import pandas as pd

quandl.ApiConfig.api_key = "_ns3bHxUkWyvcD2JknyL"

def load_pickle_data(path):
    if path.exists() and path.is_file():
        print("File exists!")
        data = pickle.load(open(path, "rb"))
        return data
    else:
        print("File not exists!")

def load_csv_data(path):
    if path.exists() and path.is_file():
        print("File exists!")
        data = pd.read_csv(path)
        return data
    else:
        print("File not exists!")


stock_symbol = ['AAPL', 'FB', 'MSFT']
date_range = ["2006-01-01", "2017-01-01"]

baes_path = os.path.dirname(os.path.dirname(os.getcwd()))
config_pickle_path = Path(os.path.join(baes_path, "env_config.pickle"))
stock_pickle_path = Path(os.path.join(baes_path, "data", "stocks.pickle"))
stock_csv_path = Path(os.path.join(baes_path, "data", "stocks.csv"))


stock_data = load_csv_data(stock_csv_path)
#print(stock_data)
stock_data = stock_data.loc[stock_data["Exchange"].isin(['NYQ', 'NMS'])]
print(stock_data["Ticker"])
print(np.array(stock_data["Ticker"]))
print(np.array(stock_data["Ticker"]).tolist())

stock_symbol.extend(np.array(stock_data["Ticker"]).tolist())
print(stock_symbol)

env_virable = load_pickle_data(config_pickle_path)
if env_virable is not None:
    price_details_path = Path(env_virable.get("PRJ_HOME_PATH"), env_virable.get("PRICE_STORE_PATH"))
    if not price_details_path.exists():
        os.mkdir(price_details_path)
    for item in stock_symbol:
        stock_quote_file = os.path.join(price_details_path,item + ".csv")
        if not Path(stock_quote_file).exists():
            print("WIKI" + "/" + item)
            try:
               mydata = quandl.get("WIKI" + "/" + item, start_date=date_range[0], end_date=date_range[1])
               mydata.to_csv(stock_quote_file)
            except:
                print("Get data failed for %s"%("WIKI" + "/" + item))
        else:
            print("%s already exists!\n"%(item))
