
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import urllib2
import requests
import os
import shutil
import pickle

folder_path = "file_download"
finished_list = []
finished = "finished.pickle"


def download_file(url, file_name):
    global finished_list
    r = requests.get(url, stream=True)
    with open(file_name, "wb") as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
    finished_list.append(file_name)
    f_pickle = open(finished, "wb")
    pickle.dump(finished_list, f_pickle)
    f_pickle.close()
    f.close()

def start_extract():
    global finished_list
    driver = webdriver.Firefox()
    driver.get("https://www.learningmarkets.com/strategy-sessions/")
    #buttont_elem = driver.find_element_by_class_name("btn btn-default dropdown-toggle")
    buttont_elem = driver.find_element_by_css_selector(".btn.btn-default.dropdown-toggle")
    buttont_elem.click()

    #subitem = driver.find_element_by_css_selector(".dropdown-menu.pull-right")
    li_list = driver.find_elements_by_css_selector(".dropdown-item.dropdown-item-button")
    for li_item in li_list:
        if li_item.text == "All":
            li_item.click()
            break

    link_list = driver.find_elements_by_tag_name("a")
    if not os.path.exists(folder_path):
        os.mkdir(folder_path)

    if os.path.exists(finished):
        f_pickle = open(finished, "rb")
        finished_list = pickle.load(f_pickle)
        f_pickle.close()

    for link_item in link_list:
        if link_item.text == "view":
            print(link_item.get_attribute("href"))
            soup = BeautifulSoup(urllib2.urlopen(link_item.get_attribute("href")), "html5lib")
            video_link = soup.find_all("source")[0]["src"]
            print(video_link)
            file_name = link_item.get_attribute("href").split("/")[-2] + ".mp4"
            url = video_link[:-4]
            original_file_name = url.split("/")[-1]
            original_file_name = original_file_name.split(".")[0]
            year = original_file_name.split("-")[-2]
            month = original_file_name.split("-")[0][2:]
            day = original_file_name.split("-")[1]
            time_stap = year + "-" + month + "-" + day + "-"
            file_name = time_stap + file_name
            file_name = os.path.join(folder_path, file_name)
            print(file_name)
            print(url)
            if file_name in finished_list:
                print("{} has already exsited".format(file_name))
                continue
            try:
                download_file(url, file_name)
            except:
                shutil.rmtree(file_name)

start_extract()
