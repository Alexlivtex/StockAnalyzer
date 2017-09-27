import requests
import bs4 as bs
import pickle
import os
import datetime as dt
import pandas_datareader.data as web
import quandl

data_path = os.path.join("data", "Training_data", "Stocks", "SP_500_data")
pickle_path = os.path.join("project_data", "sp&500_tickle.pickle")

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

    with open(pickle_path, "wb") as f:
        pickle.dump(ticker_list, f)
        f.close()

def get_data_from_sp500(reload_data=False):
    if reload_data is True:
        save_sp_500_tickers()

    if not os.path.exists(data_path):
        os.mkdir(data_path)

    with open(pickle_path, "rb") as f:
        ticker_list = pickle.load(f)

    for ticker in ticker_list:
        if not os.path.exists(os.path.join(data_path, "{}.csv".format(ticker))):
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
                    df.to_csv(os.path.join(data_path, "{}.csv".format(ticker)))
            except:
                try:
                    if len(ticker.split(".")) > 0:
                        df = web.DataReader(ticker.replace(".", "-"), "yahoo", start, end)
                    else:
                        df = web.DataReader(ticker, "yahoo", start, end)
                    df.to_csv(os.path.join(data_path, "{}.csv".format(ticker)))
                except:
                    print("================={} can not be downloaded!==================".format(ticker))
        else:
            print("{}.csv already exists".format(ticker))


def obtain_sp_data():
    if not os.path.exists(os.path.join("project_data", "sp&500_tickle.pickle")):
        save_sp_500_tickers()
    get_data_from_sp500()