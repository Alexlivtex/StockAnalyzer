import os
import env_setup

evn_var = env_setup.load_env()
if evn_var is not None:
    print(os.path.join(evn_var.get("PRJ_HOME_PATH"), evn_var.get("DATA_OBTAIN_HOME_PATH")))

    # Begin to install the ta-lib library
    os.chdir(os.path.join(evn_var.get("PRJ_HOME_PATH"), evn_var.get("DATA_OBTAIN_HOME_PATH")))
    os.system("python setup.py install")

    os.chdir(os.path.join(evn_var.get("PRJ_HOME_PATH"), evn_var.get("DATA_TICKER_DOWNLOAD_PATH")))
    os.system("python setup.py install")

    os.chdir(os.path.join(evn_var.get("PRJ_HOME_PATH"), evn_var.get("PRICE_QUOTING_PATH")))
    os.system("python setup.py install")
else:
    print("Environment is not ready, please run env_set_up to set up!")


