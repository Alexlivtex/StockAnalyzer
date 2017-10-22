from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import bs4 as bs
import pandas as pd
import os

class ContentEmptyError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

def grab_data_from_stockcharts(file_path, ticker_list):
    driver = webdriver.Firefox()
    driver.get("https://stockcharts.com/scripts/php/dblogin.php")
    elem_username = driver.find_element_by_name("form_UserID")
    elem_password = driver.find_element_by_name("form_UserPassword")
    elem_username.send_keys("XXXX")
    elem_password.send_keys("XXXX")
    elem_password.send_keys(Keys.RETURN)
    time.sleep(10)
    for ticker_item in ticker_list:
        if os.path.exists(os.path.join(file_path, "{}.csv".format(ticker_item))):
            print("{}.csv already exists".format(ticker_item))
            continue
        link = "http://stockcharts.com/h-hd/?" + ticker_item
        driver.get(link)
        try:
            element = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CLASS_NAME, "historical-data-descrip"))
            )
            soup = bs.BeautifulSoup(driver.page_source, 'lxml')
            price_table = soup.find("div", {"class" : "historical-data-descrip"})
            price_content = price_table.findAll("pre")
            data_table = price_content[0].text
            if data_table.split(" ")[2] == "not":
                raise ContentEmptyError("{}".format(ticker_item))
            data_table = data_table[3:-1]
            f = open("{}.txt".format(ticker_item), "w")
            f.write(data_table)
            f.close()
            collect_data_to_csv(file_path, ticker_item)
        except:
            print("{} can not be downloaded!".format(ticker_item))
            continue
        time.sleep(10)
    driver.quit()

def collect_data_to_csv(file_path, ticker):
    start_index = 0
    f = open("{}.txt".format(ticker), "r")
    lines = f.readlines()
    f.close()
    for index in range(len(lines)):
        if lines[index][0] == "=":
            start_index = index
            break
    lines = lines[start_index + 1:]
    columns = ["Day", "Date", "Open", "High", "Low", "Close", "Volume"]
    list_of_data = []
    print("===============================%d==============================" % (len(lines)))
    for line in lines:
        str_tmp = ' '.join(line.split())
        # list_tmp = str_tmp.split(" ")
        list_of_data.append(str_tmp.split(" "))

    df = pd.DataFrame(list_of_data, columns=columns)
    df = df[["Date", "Open", "High", "Low", "Close", "Volume"]]
    df.set_index('Date', inplace=True)
    df = df.iloc[::-1]
    df.to_csv(os.path.join(file_path, "{}.csv".format(ticker)))
    os.remove("{}.txt".format(ticker))

