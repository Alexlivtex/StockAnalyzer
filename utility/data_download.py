from pathlib import Path
import quandl
import os
import datetime as dt
import pandas_datareader.data as web

class ContentEmptyError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

def data_download(ticker_list, csv_path, date_range):
    for ticker in ticker_list:
        if not Path(os.path.join(csv_path, "{}.csv".format(ticker))).exists():
            print("WIKI" + "/" + ticker)
            try:
                if len(ticker.split(".")) > 0:
                    mydata = quandl.get("WIKI" + "/" + ticker.replace(".", "_"), start_date=date_range[0],
                                        end_date=date_range[1])
                else:
                    mydata = quandl.get("WIKI" + "/" + ticker, start_date=date_range[0], end_date=date_range[1])

                if len(mydata["Date"]) == 0:
                    raise ContentEmptyError("{}".format(ticker))
                mydata.to_csv(csv_path)
            except:
                print("Get data failed for %s" % (ticker))
        else:
            print("%s already exists!\n" % (ticker))