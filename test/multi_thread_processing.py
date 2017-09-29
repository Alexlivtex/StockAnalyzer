import math
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import bs4 as bs
from selenium.webdriver.common.by import By
import threading

class ContentEmptyError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

def obtain_data(ticker_list = []):
    driver = webdriver.Firefox()
    driver.get("https://stockcharts.com/scripts/php/dblogin.php")
    elem_username = driver.find_element_by_name("form_UserID")
    elem_password = driver.find_element_by_name("form_UserPassword")
    elem_username.send_keys("XXXXXXXXX@XX.com")
    elem_password.send_keys("XXXXXXXXXXXXX")
    elem_password.send_keys(Keys.RETURN)
    time.sleep(10)
    for ticker_item in ticker_list:
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
        except:
            print("{} can not be downloaded!".format(ticker_item))
            continue
        time.sleep(10)
    driver.quit()

def list_chunks(ticker_list, sub_count):
    for i in range(0, len(ticker_list), sub_count):
        yield ticker_list[i:i + sub_count]


def main():
    test_list = ["AAPL", "BABA", "JD", "AMRS", "FB", "MMM", "ATVI", "ADBE", "GOOG", "AMZN"]

    max_thread_count = 5


    final_list = list(list_chunks(test_list, math.ceil(len(test_list) / max_thread_count)))
    threads = []

    for i in range(max_thread_count):
        threads.append(threading.Thread(target=obtain_data, args=([final_list[i]])))

    for t in threads:
        t.setDaemon(True)
        time.sleep(5)
        t.start()

    for thread_index in threads:
        thread_index.join()
