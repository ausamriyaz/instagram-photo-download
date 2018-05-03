import time

import os

import wget
from selenium import webdriver
from bs4 import BeautifulSoup
import re

chrome_options = webdriver.ChromeOptions()
prefs = {"profile.default_content_setting_values.notifications": 2}
chrome_options.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome(chrome_options=chrome_options)
driver.set_page_load_timeout(30)
link = "link"
driver.get(link)
##scrolling
driver.execute_script(
    "var lastScrollHeight = 0;function autoScroll() {var sh = document.documentElement.scrollHeight;if (sh != lastScrollHeight) {lastScrollHeight = sh;document.documentElement.scrollTop = sh;}}window.setInterval(autoScroll, 100);")
time.sleep(10)
html = driver.page_source
alllist = []

if "This Account is Private" in html:

    print("the account is private!!")

else:
    links = re.findall(r'http(.*?)jpg', html, re.DOTALL)
    for n in links:
        if "s640x640" in n:
            alllist.append("http" + n + "jpg")

    uniquelist = list(set(alllist))
    x = 1

    current_directory = os.getcwd()
    final_directory = os.path.join(current_directory, r'new folder')
    if not os.path.exists(final_directory):
        os.makedirs(final_directory)

    for n in uniquelist:
        wget.download(n, current_directory + '/new folder/' + str(x) + '.jpg')
        x += 1
