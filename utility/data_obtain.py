from pathlib import Path
import pandas as pd
import os
import numpy as np
import quandl

import pandas as pd
import pandas_datareader.data as web
import datetime as dt

quandl.ApiConfig.api_key = "_ns3bHxUkWyvcD2JknyL"
stock_list = []

date_range = ["2006-01-01", "2017-01-01"]

class ContentEmptyError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

def load_csv_data(path):
    if Path(path).exists() and Path(path).is_file():
        print("File exists!")
        data = pd.read_csv(path)
        return data
    else:
        print("File not exists!")

def complete_obtain_data():
    stock_csv_path = os.path.join("project_data", "stocks.csv")
    stock_data = load_csv_data(stock_csv_path)
    # print(stock_data)
    stock_data = stock_data.loc[stock_data["Exchange"].isin(['NYQ', 'NMS'])]
    print(stock_data["Ticker"])
    print(np.array(stock_data["Ticker"]))
    print(np.array(stock_data["Ticker"]).tolist())
    stock_list.extend(np.array(stock_data["Ticker"]).tolist())

    price_details_path = os.path.join("data", "Complete_data", "stocks")
    error_list = []
    if not Path(price_details_path).exists():
        os.mkdir(price_details_path)
    for item in stock_list:
        stock_quote_file = os.path.join(price_details_path, item + ".csv")
        if not Path(stock_quote_file).exists():
            print("WIKI" + "/" + item)
            try:
               if len(item.split(".")) > 0:
                   mydata = quandl.get("WIKI" + "/" + item.replace(".", "_"), start_date=date_range[0], end_date=date_range[1])
               else:
                   mydata = quandl.get("WIKI" + "/" + item, start_date=date_range[0], end_date=date_range[1])

               if len(mydata["Date"]) == 0:
                   raise ContentEmptyError("{}".format(item))
               mydata.to_csv(stock_quote_file)
            except:
                start = dt.datetime(2006,1, 1)
                end = dt.datetime(2017,1,1)
                try:
                    if len(item.split(".")) > 0:
                        df = web.DataReader(item.replace(".", "-"), 'yahoo', start, end)
                    else:
                        df = web.DataReader(item, 'yahoo', start, end)
                    df.to_csv(stock_quote_file)
                except:
                    error_list.append(item)
                    print("Get data failed for %s"%(item))
        else:
            print("%s already exists!\n"%(item))
    f = open(os.path.join("project_data", "result_list"), "w")
    for error_item in error_list:
        f.writelines(error_item)
    f.close()