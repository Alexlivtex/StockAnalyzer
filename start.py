#!/usr/bin/env python

import pickle
from time import sleep
import argparse
import io
import os
import pandas as pd
import numpy as np
import math

from ticker_downloader.downloader.StockDownloader import StockDownloader
from ticker_downloader.downloader.ETFDownloader import ETFDownloader
from ticker_downloader.downloader.FutureDownloader import FutureDownloader
from ticker_downloader.downloader.IndexDownloader import IndexDownloader
from ticker_downloader.downloader.MutualFundDownloader import MutualFundDownloader
from ticker_downloader.downloader.CurrencyDownloader import CurrencyDownloader
from ticker_downloader.compat import text
from ticker_downloader.compat import csv

from utility.stockcharts_obtain import grab_data_from_stockcharts
from utility.SP500_obtain import obtain_sp_data
import threading

import tablib

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

def list_chunks(ticker_list, sub_count):
    for i in range(0, len(ticker_list), sub_count):
        yield ticker_list[i:i + sub_count]

if __name__ == "__main__":
    complete_data_path = os.path.join("data", "Complete_data", "stocks")
    training_data_path = os.path.join("data", "Training_data", "Stocks", "SP_500_data")
    stock_list = []
    sp_500_list = []

    threads_complte = []
    threads_sp500 = []
    max_thread_count = 5

    # Check the stock ticker
    main()

    # Get all the stock data and store it local
    stock_data = pd.read_csv(os.path.join("project_data", "stocks.csv"))
    stock_data = stock_data.loc[stock_data["Exchange"].isin(['NYQ', 'NMS'])]
    print(stock_data["Ticker"])
    print(np.array(stock_data["Ticker"]))
    print(np.array(stock_data["Ticker"]).tolist())
    stock_list.extend(np.array(stock_data["Ticker"]).tolist())
    final_list_complete = list(list_chunks(stock_list, math.ceil(len(stock_list) / max_thread_count)))
    for i in range(max_thread_count):
        threads_complte.append(threading.Thread(target=grab_data_from_stockcharts, args=(complete_data_path, final_list_complete[i])))
        #grab_data_from_stockcharts(complete_data_path, stock_list)

    for t in threads_complte:
        t.setDaemon(True)
        sleep(10)
        t.start()

    for thread_index in threads_complte:
        thread_index.join()

    # Downloading the SP&500 data
    obtain_sp_data()
    f_SP_500 = open(os.path.join("project_data", "sp&500_tickle.pickle"), "rb")
    sp_500_list = pickle.load(f_SP_500)
    final_list_sp500 = list(list_chunks(sp_500_list, math.ceil(len(sp_500_list) / max_thread_count)))

    for i in range(max_thread_count):
        threads_sp500.append(threading.Thread(target=grab_data_from_stockcharts, args=(training_data_path, final_list_sp500[i])))

    for t_sp in threads_sp500:
        t_sp.setDaemon(True)
        sleep(10)
        t_sp.start()

    for thread_index_sp in threads_sp500:
        thread_index_sp.join()