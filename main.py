import time

import os

import wget
from PIL import Image
from selenium import webdriver
import re

from selenium.common.exceptions import NoSuchElementException

chrome_options = webdriver.ChromeOptions()
prefs = {"profile.default_content_setting_values.notifications": 2}
chrome_options.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome(chrome_options=chrome_options)
driver.set_page_load_timeout(30)


def sort():
    current_directory = os.getcwd()

    Path = os.path.join(current_directory + '/new folder/')
    filelist = os.listdir(Path)
    x = []
    for i in filelist:
        with Image.open(Path + i) as img:
            width, height = img.size
            x.append(str(width) + "x" + str(height))

    uniquelist = list(set(x))

    for u in uniquelist:

        final_directory = os.path.join(current_directory + '/new folder/', r'' + u)
        if not os.path.exists(final_directory):
            os.makedirs(final_directory)

    for i in filelist:
        width = 0
        height = 0
        with Image.open(Path + i) as img:
            width, height = img.size
            img.close()
        os.rename(Path + i, Path + str(width) + "x" + str(height) + "/" + i)


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
            print(str(x)+" - "+n)
            wget.download(n, current_directory + '/new folder/' + str(x) + '.jpg')
            x += 1
    sort()
    print("time taken: "+str(time.time()-starttime))



options()
