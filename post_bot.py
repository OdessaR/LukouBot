#! /usr/bin/python3
# -*- coding: UTF-8 -*-
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import requests
import json
import csv
import pandas as pd 
import os.path
import datetime
from selenium.webdriver.common.keys import Keys
from selenium import webdriver

def post_func():
    # browser = webdriver.Chrome()
    chrome_options = Options()  
    # chrome_options.add_argument("--headless") 
    browser = webdriver.Chrome(chrome_options=chrome_options)

    browser.get("http://www.lukou.com")
    browser.find_element_by_class_name("login").click()
    browser.find_element_by_id("email").send_keys("your account")
    browser.find_element_by_id ("password").send_keys("your password")
    browser.find_element_by_id("loginSubmit").click()
    time.sleep(3)
    browser.get("http://www.lukou.com/post/blog")
    time.sleep(1)
    title_element = browser.find_element_by_css_selector("#form > div > div > div.title > input")
    #today:my_date = datetime.date.today().strftime('_%m%d')
    today = datetime.date.today().strftime('%m%d')
    title_element.send_keys(today)
    time.sleep(3)

    # browser.close()

    # read in the result list of today
    today_result = 'result_'+str(today) + '.csv'
    df_result = pd.read_csv(today_result,header=0)

    # loop through the dataframe
    tuan_text = ''
    for i in range (0,len(df_result)):
        for tuan in df_result:
            tuan_text = tuan_text + str(df_result[tuan][i]) + '<br>'
    print(tuan_text)
    
    # write the information in text area
    text_element = browser.find_element_by_css_selector('.simditor .simditor-body')
    text_element.send_keys(tuan_text)
    time.sleep(1)
    # send out the post
    browser.find_element_by_css_selector("#form > div > div > div.action > div > button.active.publish").click()
    time.sleep(1)

    # edit the post
    browser.get('http://www.lukou.com/circle')
    time.sleep(1)
    browser.get(browser.find_element_by_css_selector('.feed-wrap:first-child a.edit').get_attribute("href"))
    time.sleep(1)
    # edit post content again
    edit_post_element = browser.find_element_by_css_selector('.simditor .simditor-body')
    edit_post_element.send_keys(Keys.CONTROL, 'a') #highlight all in box
    time.sleep(1)
    edit_post_element.send_keys(Keys.CONTROL, 'x') #copy
    time.sleep(1)
    edit_post_element.send_keys(Keys.CONTROL, 'v') #paste
    time.sleep(1)
    # post
    browser.find_element_by_css_selector("#form > div > div > div.action > div > button.active.publish").click()
    # send message to telegram after posting
    send_message("Successfully posted for " + today)

def send_message(msg):
    url = " your telegram token" + msg
    requests.get(url)

post_func()