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

def obtain_sp_data():
    if not os.path.exists(pickle_path):
        save_sp_500_tickers()