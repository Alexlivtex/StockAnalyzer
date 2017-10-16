from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import urllib2

def start_extract():
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
    for link_item in link_list:
        if link_item.text == "view":
            print link_item.get_attribute("href")
            soup = BeautifulSoup(urllib2.urlopen(link_item.get_attribute("href")), "html5lib")
            print(soup.find_all("source")[0]["src"])

start_extract()
