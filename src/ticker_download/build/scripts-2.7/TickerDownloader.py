#!C:\Python27\python.exe

import pickle
from time import sleep
import argparse
import io

from ytd.downloader.StockDownloader import StockDownloader
from ytd.downloader.ETFDownloader import ETFDownloader
from ytd.downloader.FutureDownloader import FutureDownloader
from ytd.downloader.IndexDownloader import IndexDownloader
from ytd.downloader.MutualFundDownloader import MutualFundDownloader
from ytd.downloader.CurrencyDownloader import CurrencyDownloader
from ytd.compat import text
from ytd.compat import csv
from collections import namedtuple


import tablib

import sys

class Struct:
    def __init__(self, **entries):
        self.__dict__.update(entries)

        
options = {
    "stocks": StockDownloader(),
    "etf": ETFDownloader(),
    "future": FutureDownloader(),
    "index": IndexDownloader(),
    "mutualfund": MutualFundDownloader(),
    "currency": CurrencyDownloader(),
}

argument_parameter = {
    "insecure":"",
    "export" : "",
    "type" : "all",
    "market" : "",
    "sleep" : 1,
    "pandantic" : "",
    "Exchange" : "",
}

DATA_PATH = "../../data/"


def loadDownloader(tickerType):
    with open(DATA_PATH + tickerType + ".pickle", "rb") as f:
        return pickle.load(f)


def saveDownloader(downloader, tickerType):
    with open(DATA_PATH+ tickerType + ".pickle", "wb") as f:
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


def execute(args):
    downloader = None
    if args.insecure:
        print("Using insecure connection")

    if args.export:
        print("Exporting pickle file")
    print(args.type)
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

        with io.open(DATA_PATH + downloader.type + '.csv', 'w', encoding='utf-8') as f:
            f.write(text.join(u',', data.headers) + '\n')
            writer = csv.writer(f)
            for i in range(0, len(data)):
                row = [text(y) if not y is None else u"" for y in data[i]]
                writer.writerow(row)

        with open(DATA_PATH + downloader.type + '.xlsx', 'wb') as f:
            f.write(data.xlsx)

        with open(DATA_PATH + downloader.type + '.json', 'wb') as f:
            f.write(data.json.encode('UTF-8'))

        with open(DATA_PATH + downloader.type + '.yaml', 'wb') as f:
            f.write(data.yaml.encode('UTF-8'))    

def main():
    args = argument_parameter.copy()
    if args["type"] == "all":
        for item in options:
            args["type"] = item;
            execute(Struct(**args))

if __name__ == "__main__":
    main()
