from pathlib import Path
import quandl
import datetime as dt
import pandas_datareader.data as web

class ContentEmptyError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

date_range = ["2006-01-01", "2017-01-01"]

def data_download(ticker, csv_path):
    if not Path(csv_path).exists():
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
            start = dt.datetime(2006, 1, 1)
            end = dt.datetime(2017, 1, 1)
            try:
                if len(ticker.split(".")) > 0:
                    df = web.DataReader(ticker.replace(".", "-"), 'yahoo', start, end)
                else:
                    df = web.DataReader(ticker, 'yahoo', start, end)
                df.to_csv(csv_path)
            except:
                print("Get data failed for %s" % (ticker))
    else:
        print("%s already exists!\n" % (ticker))