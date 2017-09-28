import os
import pandas as pd
import talib
import numpy as np
import matplotlib.pyplot as plt

def caculate_indicator(path):
    list_file = os.listdir(path)
    print(list_file)
    for file_item in list_file:
        fila_path = os.path.join(path, file_item)
        df = pd.read_csv(fila_path)
        open = np.asarray(df["Open"])
        high = np.asarray(df["High"])
        low = np.asarray(df["Low"])
        close = np.asarray(df["Close"])
        volume = np.asarray(df["Volume"], dtype='float')

        df['SMA_200'] = talib.SMA(close, 200)
        df['SMA_10'] = talib.SMA(close, 10)
        df['SMA_30'] = talib.SMA(close, 30)
        df['SMA_50'] = talib.SMA(close, 50)
        upperband, middleband, lowerband = talib.BBANDS(close, timeperiod=5, nbdevup=2, nbdevdn=2, matype=0)
        df['upperband'] = upperband
        df['middleband'] = middleband
        df['lowerband'] = lowerband

        df["HT_TRENDLINE"] = talib.HT_TRENDLINE(close)

        df["ADX"] = talib.ADX(high, low, close, timeperiod=14)
        df["ADXR"] = talib.ADXR(high, low, close, timeperiod=14)
        df["APO"] = talib.APO(close, fastperiod=12, slowperiod=26, matype=0)

        aroondown, aroonup = talib.AROON(high, low, timeperiod=14)
        df["aroondown"] = aroondown
        df["aroonup"] = aroonup

        df["AROONOSC"] = talib.AROONOSC(high, low, timeperiod=14)
        df["BOP"] =  talib.BOP(open, high, low, close)
        df["CCI"] = talib.CCI(high, low, close, timeperiod=14)
        df["CMO"] = talib.CMO(close, timeperiod=14)
        df["DX"] =  talib.DX(high, low, close, timeperiod=14)
        macd, macdsignal, macdhist = talib.MACD(close, fastperiod=12, slowperiod=26, signalperiod=9)
        df["macd"] = macd
        df["macdsignal"] = macdsignal
        df["macdhist"] = macdhist

        # macd, macdsignal, macdhist = MACDEXT(close, fastperiod=12, fastmatype=0, slowperiod=26, slowmatype=0, signalperiod=9, signalmatype=0)
        # macd, macdsignal, macdhist = MACDFIX(close, signalperiod=9)


        df["MFI"] = talib.MFI(high, low, close, volume, timeperiod=14)
        df["MINUS_DI"] = talib.MINUS_DI(high, low, close, timeperiod=14)
        df["MINUS_DM"] = talib.MINUS_DM(high, low, timeperiod=14)
        df["MOM"] = talib.MOM(close, timeperiod=10)
        df["PLUS_DI"] = talib.PLUS_DI(high, low, close, timeperiod=14)
        df["PLUS_DM"] = talib.PLUS_DM(high, low, timeperiod=14)
        df["PPO"] = talib.PPO(close, fastperiod=12, slowperiod=26, matype=0)
        df["ROC"] = talib.ROC(close, timeperiod=10)
        df["ROCP"] = talib.ROCP(close, timeperiod=10)
        df["ROCR"] = talib.ROCR(close, timeperiod=10)
        df["ROCR100"] = talib.ROCR100(close, timeperiod=10)
        df["RSI"] = talib.RSI(close, timeperiod=14)
        slowk, slowd = talib.STOCH(high, low, close, fastk_period=5, slowk_period=3, slowk_matype=0, slowd_period=3, slowd_matype=0)
        df["slowk"] = slowk
        df["slowd"] = slowd

        # fastk, fastd = STOCHF(high, low, close, fastk_period=5, fastd_period=3, fastd_matype=0)
        fastk, fastd = talib.STOCHRSI(close, timeperiod=14, fastk_period=5, fastd_period=3, fastd_matype=0)
        df["fastk"] = fastk
        df["fastd"] = fastd

        df["TRIX"] = talib.TRIX(close, timeperiod=30)
        df["ULTOSC"] = talib.ULTOSC(high, low, close, timeperiod1=7, timeperiod2=14, timeperiod3=28)
        df["WILLR"] = talib.WILLR(high, low, close, timeperiod=14)

        # ================Volume Indicator Functions=================
        df["AD"] = talib.AD(high, low, close, volume)
        df["ADOSC"] = talib.ADOSC(high, low, close, volume, fastperiod=3, slowperiod=10)
        df["OBV"] = talib.OBV(close, volume)

        # =================Volatility Indicator Functions======================
        df["ATR"] = talib.ATR(high, low, close, timeperiod=14)
        df["NATR"] = talib.NATR(high, low, close, timeperiod=14)
        df["TRANGE"] = talib.TRANGE(high, low, close)

        # =======================Price Transform Functions=====================
        df["AVGPRICE"] = talib.AVGPRICE(open, high, low, close)
        df["MEDPRICE"] = talib.MEDPRICE(high, low)
        df["TYPPRICE"] = talib.TYPPRICE(high, low, close)
        df["WCLPRICE"] = talib.WCLPRICE(high, low, close)

        # =================Cycle Indicator Functions======================
        df["HT_DCPERIOD"] = talib.HT_DCPERIOD(close)
        df["HT_DCPHASE"] = talib.HT_DCPHASE(close)
        inphase, quadrature = talib.HT_PHASOR(close)
        df["inphase"] = inphase
        df["quadrature"] = quadrature

        sine, leadsine = talib.HT_SINE(close)
        df["sine"] = sine
        df["leadsine"] = leadsine

        df["HT_TRENDMODE"] = talib.HT_TRENDMODE(close)
        df.set_index('Date', inplace=True)
        df = df[210:]
        df.to_csv(fila_path)

caculate_indicator("/root/Source/StockAnalyzer/data/Complete_data/stocks")
