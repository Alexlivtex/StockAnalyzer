import os
from pathlib import Path
import pickle

env_variable = {
       "PRJ_HOME_PATH" :  os.getcwd(),
       "DATA_OBTAIN_HOME_PATH" : os.path.join("src" , "data_obtain"),
       "DATA_TICKER_DOWNLOAD_PATH" : os.path.join("src", "ticker_download"),
       "PRICE_QUOTING_PATH" : os.path.join("src", "price_quoting"),
       "PRICE_STORE_PATH" : os.path.join("data", "price_details"),
}

pickle_file = Path("env_config.pickle")

def write_env():
    if pickle_file.exists() and pickle_file.is_file():
        os.remove(pickle_file)
    with open("env_config.pickle", "wb") as f:
        pickle.dump(env_variable, file=f, protocol=pickle.HIGHEST_PROTOCOL)


def load_env():
    if pickle_file.exists() and pickle_file.is_file():
        data_project = pickle.load(open("env_config.pickle", "rb"))
        return data_project
    else:
        write_env()
        print("Environment variable has not been set, just ready, you should run again!\n")
        return

write_env()

