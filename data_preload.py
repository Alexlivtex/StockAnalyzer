import os
import pickle
from pathlib import Path
pickle_file = Path("env_config.pickle")

if pickle_file.exists():
    data = pickle.load(open(pickle_file, "rb"))
    print(data)

os.chdir(os.path.join(data.get("PRJ_HOME_PATH"), data.get("DATA_TICKER_DOWNLOAD_PATH")))
os.system("python TickerDownloader.py stocks")
