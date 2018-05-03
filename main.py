import time

import os

import wget
from selenium import webdriver
import re

from selenium.common.exceptions import NoSuchElementException

chrome_options = webdriver.ChromeOptions()
prefs = {"profile.default_content_setting_values.notifications": 2}
chrome_options.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome(chrome_options=chrome_options)
driver.set_page_load_timeout(30)



def options():
    print("1. log in to download a friend's profile")
    print("2. download a public profile")
    inp=input("choice: ")
    if inp=="1":
        login()
    elif inp=="2":
        temp = input("enter instagram username of the profile: ")
        while temp == "":
            temp = input("enter instagram username of the profile: ")
        download("https://www.instagram.com/" + temp + "/")
    else:
        print("the choice doesnt exist")
        options()

def login():
    driver.get("https://www.instagram.com/accounts/login/")
    name = input("username: ")
    while name=="":
        name = input("username: ")

    pasword= input('Password:')
    while pasword=="":
        pasword = input('Password:')

    driver.find_element_by_name("username").send_keys(name)

    driver.find_element_by_name("password").send_keys(pasword)
    driver.find_element_by_xpath("//*[contains(text(), 'Log in')]").click()
    time.sleep(5)

    try:
        err = driver.find_element_by_id("slfErrorAlert")
    except NoSuchElementException:
        print("login successful")
        temp= input("enter instagram username of the profile: ")
        while temp=="":
            temp = input("enter instagram username of the profile: ")

        download("https://www.instagram.com/"+temp+"/")

    else:
        print("error: Please check your username and password try again.")
        login()



def download(link):


    driver.get(link)
    ##scrolling

    starttime= time.time()
    lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
    match = False
    while (match == False):
        lastCount = lenOfPage
        time.sleep(3)
        lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
        if lastCount == lenOfPage:
            match = True


    html = driver.page_source
    alllist = []

    if "This Account is Private" in html:

        print("the account is private!!")

    elif "this page isn't available" in html:
        print("this page isn't available")


    else:
        links = re.findall(r'http(.*?)jpg', html, re.DOTALL)
        for n in links:
            if "e35" in n:
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

    print("time taken: "+str(time.time()-starttime))



options()
'''
s150x150
s240x240
s320x320

"https://instagram.fcmb1-1.fna.fbcdn.net/vp/cac3363d82449bba8b01d7b8b16ad967/5B9B9073/t51.2885-15/s320x320/e35/c0.109.927.927/28153927_539532719763942_7795927771854667776_n.jpg"
"https://instagram.fcmb1-1.fna.fbcdn.net/vp/df51aa78c729bf8ead6971fd1cbb41d9/5B78A69B/t51.2885-15/s240x240/e35/c0.109.927.927/28153927_539532719763942_7795927771854667776_n.jpg"
'''