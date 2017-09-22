import requests
import bs4 as bs
import pickle
import os
import datetime as dt
import pandas_datareader.data as web
import quandl
import pandas as pd

def check_null():
    f_pickle = open("sp&500_tick.pickle", "rb")
    ticker_list = pickle.load(f_pickle)
    for ticker_item in ticker_list:
        if os.path.exists("SP_500_data/{}.csv".format(ticker_item)):
            df = pd.read_csv("SP_500_data/{}.csv".format(ticker_item))
            count = 0
            for null_count in df.isnull().sum():
                count += null_count
            if count > 0 or len(df['Date']) == 0:
                print("{}.csv has some missing value".format(ticker_item))
                os.remove("SP_500_data/{}.csv".format(ticker_item))

class ContentEmptyError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)


def save_sp_500_tickers():
    resp = requests.get('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    soup = bs.BeautifulSoup(resp.text, 'lxml')
    table = soup.find("table", {"class": "wikitable sortable"})
    ticker_list = []
    for row in table.findAll("tr")[1:]:
        ticker = row.findAll("td")[0].text
        ticker_list.append(ticker)

    with open("sp&500_tick.pickle", "wb") as f:
        pickle.dump(ticker_list, f)
        f.close()

def get_data_from_sp500(reload_data=False):
    if reload_data is True:
        save_sp_500_tickers()

    if not os.path.exists("SP_500_data"):
        os.mkdir("SP_500_data")

    with open("sp&500_tick.pickle", "rb") as f:
        ticker_list = pickle.load(f)

    for ticker in ticker_list:
        if not os.path.exists("SP_500_data/{}.csv".format(ticker)):
            start = dt.datetime(2006, 1, 1)
            end = dt.datetime(2017,1,1)
            try:
                if len(ticker.split(".")) > 0:
                    df = quandl.get("WIKI/{}".format(ticker.replace(".", "_")), start_date="2006-01-01",end_date="2017-01-01")
                else:
                    df = quandl.get("WIKI/{}".format(ticker), start_date="2006-01-01", end_date="2017-01-01")

                if len(df["Date"]) == 0:
                    raise ContentEmptyError("{}".format(ticker))
                else:
                    df.to_csv("SP_500_data/{}.csv".format(ticker))
            except:
                try:
                    if len(ticker.split(".")) > 0:
                        df = web.DataReader(ticker.replace(".", "-"), "yahoo", start, end)
                    else:
                        df = web.DataReader(ticker, "yahoo", start, end)
                    df.to_csv("SP_500_data/{}.csv".format(ticker))
                except:
                    print("================={} can not be downloaded!==================".format(ticker))
        else:
            print("SP_500_data/{}.csv already exists".format(ticker))



while True:
    check_null()
    file_list = os.listdir("SP_500_data")
    f_ticker = open("sp&500_tick.pickle", "rb")
    ticker_list = pickle.load(f_ticker)
    if len(file_list) != len(ticker_list):
        get_data_from_sp500()
    else:
        break
