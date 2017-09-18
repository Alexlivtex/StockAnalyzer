#!/usr/bin/env python

import pickle
from time import sleep
import argparse
import io
from pathlib import Path
import os
import numpy as np

from ticker_downloader.downloader.StockDownloader import StockDownloader
from ticker_downloader.downloader.ETFDownloader import ETFDownloader
from ticker_downloader.downloader.FutureDownloader import FutureDownloader
from ticker_downloader.downloader.IndexDownloader import IndexDownloader
from ticker_downloader.downloader.MutualFundDownloader import MutualFundDownloader
from ticker_downloader.downloader.CurrencyDownloader import CurrencyDownloader
from ticker_downloader.compat import text
from ticker_downloader.compat import csv

import tablib
import quandl

import pandas as pd
import pandas_datareader.data as web
import datetime as dt

quandl.ApiConfig.api_key = "_ns3bHxUkWyvcD2JknyL"
import sys

date_range = ["2006-01-01", "2017-01-01"]
stock_list = []

options = {
    "stocks": StockDownloader(),
    "etf": ETFDownloader(),
    "future": FutureDownloader(),
    "index": IndexDownloader(),
    "mutualfund": MutualFundDownloader(),
    "currency": CurrencyDownloader(),
}

PATH = "project_data"

def loadDownloader(tickerType):
    with open((os.path.join(PATH, tickerType + ".pickle")), "rb") as f:
        return pickle.load(f)


def saveDownloader(downloader, tickerType):
    with open((os.path.join(PATH, tickerType + ".pickle")), "wb") as f:
        pickle.dump(downloader, file=f, protocol=pickle.HIGHEST_PROTOCOL)


def downloadEverything(downloader, tickerType, insecure, sleeptime, pandantic, market):

    loop = 0
    while not downloader.isDone():

        symbols = downloader.nextRequest(insecure, pandantic, market)
        print("Got " + str(len(symbols)) + " downloaded " + downloader.type + " symbols:")
        if(len(symbols) > 2):
            try:
                print (" " + text(symbols[0]))
                print (" " + text(symbols[1]))
                print ("  ect...")
            except:
                print (" Could not display some ticker symbols due to char encoding")
        downloader.printProgress()

        # Save download state occasionally.
        # We do this in case this long running is suddenly interrupted.
        loop = loop + 1
        if loop % 200 == 0:
            print ("Saving downloader to disk...")
            saveDownloader(downloader, tickerType)
            print ("Downloader successfully saved.")
            print ("")

        if not downloader.isDone():
            sleep(sleeptime)  # So we don't overload the server.

def main():
    downloader = None

    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--insecure", help="use HTTP instead of HTTPS", action="store_true")
    parser.add_argument("-e", "--export", help="export immediately without downloading (Only useful if you already downloaded something to the .pickle file)", action="store_true")
    parser.add_argument('-E', '--Exchange', help='Only export ticker symbols from this exchange (the filtering is done during the export phase)')
    parser.add_argument('type', help='The type to download, this can be: '+" ".join(list(options.keys())))
    parser.add_argument("-s", "--sleep", help="The time to sleep in seconds between requests", type=float, default=0)
    parser.add_argument("-p", "--pandantic", help="Stop and warn the user if some rare assertion fails", action="store_true")
    parser.add_argument("-m", "--market", help="Specify the Region of queried exchanges (us = USA+Canada, dr=Germany, fr=France, hk=Hongkong, gb=United Kingdom, default= all)", default="all")

    args = parser.parse_args()

    if args.insecure:
        print("Using insecure connection")

    if args.export:
        print("Exporting pickle file")

    tickerType = args.type = args.type.lower()

    market = args.market = args.market.lower()

    print("Checking if we can resume a old download session")
    try:
        downloader = loadDownloader(tickerType)
        print("Downloader found on disk, resuming")
    except:
        print("No old downloader found on disk")
        print("Starting a new session")
        if tickerType not in options:
            print("Error: " + tickerType + " is not a valid type option. See --help")
            exit(1)
        else:
            downloader = options[tickerType]

    try:
        if not args.export:
            if not downloader.isDone():
                print("Downloading " + downloader.type)
                print("")
                downloadEverything(downloader, tickerType, args.insecure, args.sleep, args.pandantic, market)
                print ("Saving downloader to disk...")
                saveDownloader(downloader, tickerType)
                print ("Downloader successfully saved.")
                print ("")
            else:
                print("The downloader has already finished downloading everything")
                print("")

    except Exception as ex:
        print("A exception occurred while downloading. Suspending downloader to disk")
        saveDownloader(downloader, tickerType)
        print("Successfully saved download state")
        print("Try removing {type}.pickle file if this error persists")
        print("Issues can be reported on https://github.com/Benny-/Yahoo-ticker-symbol-downloader/issues")
        print("")
        raise
    except KeyboardInterrupt as ex:
        print("Suspending downloader to disk as .pickle file")
        saveDownloader(downloader, tickerType)

    if downloader.isDone() or args.export:
        print("Exporting "+downloader.type+" symbols")

        data = tablib.Dataset()
        data.headers = downloader.getRowHeader()

        for symbol in downloader.getCollectedSymbols():
            if(args.Exchange == None):
                data.append(symbol.getRow())
            elif (symbol.exchange == args.Exchange):
                data.append(symbol.getRow())

        with io.open((os.path.join(PATH, downloader.type + '.csv')), 'w', encoding='utf-8') as f:
            f.write(text.join(u',', data.headers) + '\n')
            writer = csv.writer(f)
            for i in range(0, len(data)):
                row = [text(y) if not y is None else u"" for y in data[i]]
                writer.writerow(row)

        with open((os.path.join(PATH, downloader.type + '.xlsx')), 'wb') as f:
            f.write(data.xlsx)

        with open((os.path.join(PATH, downloader.type + '.json')), 'wb') as f:
            f.write(data.json.encode('UTF-8'))

        with open((os.path.join(PATH, downloader.type + '.yaml')), 'wb') as f:
            f.write(data.yaml.encode('UTF-8'))


def load_csv_data(path):
    if Path(path).exists() and Path(path).is_file():
        print("File exists!")
        data = pd.read_csv(path)
        return data
    else:
        print("File not exists!")

def obtain_data():
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
               mydata = quandl.get("WIKI" + "/" + item, start_date=date_range[0], end_date=date_range[1])
               mydata.to_csv(stock_quote_file)
            except:
                start = dt.datetime(2006,1, 1)
                end = dt.datetime(2017,1,1)
                try:
                    df = web.DataReader(item, 'yahoo', start, end)
                    df.to_csv(stock_quote_file)
                except:
                    error_list.append(item)
                    print("Get data failed for %s"%("WIKI" + "/" + item))
        else:
            print("%s already exists!\n"%(item))
    f = open(os.path.join("project_data", "result_list"), "w")
    for error_item in error_list:
        f.writelines(error_item)
    f.close()

if __name__ == "__main__":
    main()
    obtain_data()
