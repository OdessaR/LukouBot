#! /usr/bin/python3
# -*- coding: UTF-8 -*-
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import requests
import json
import csv
import re
import os
import pandas as pd 
import os.path
import datetime
from datetime import datetime as dt
from selenium.webdriver.common.keys import Keys
from selenium import webdriver

def get_all_tuan(browser,query):
    #query = "&page=0"
    browser.get("http://www.lukou.com/search?q=%E5%9B%A2&s=4" + query)
    tuan_name_list = browser.find_elements_by_css_selector("div.feed-hd > div.title > a")
    #tuan_start_time_list = browser.find_elements_by_css_selector("div.feed-hd > div.author > a.time.binded-update")
    tuan_leader_list = browser.find_elements_by_css_selector("div.feed-hd > div.author > a:nth-child(1)")
    tuan_remain_list = browser.find_elements_by_css_selector("div.feed-bd > div.tuan-info > div.tuan-state")
    tuan_pic_list = browser.find_elements_by_css_selector("div.tuan-img > a > img")

    tuan_link_list = []
    tuan_start_time_list = []
    for tuan_link in browser.find_elements_by_css_selector("div.feed-desc > div.feed-hd > div.title > a"):
        link = tuan_link.get_attribute('href')
        tuan_link_list.append(link)
    for tuan_start_time in browser.find_elements_by_css_selector("a.time.binded-update"):
        date = int(tuan_start_time.get_attribute('data-time'))/1000
        new_date = dt.utcfromtimestamp(int(date)).strftime('%m%d')
        tuan_start_time_list.append(new_date)
    result = []
    tuan_name_l = []
    for tuan_name in tuan_name_list:
        name = tuan_name.text
        tuan_name_l.append(name)
    tuan_leader_l = []
    for tuan_leader in tuan_leader_list:
        leader = tuan_leader.text
        tuan_leader_l.append(leader)
    # tuan_start_time_l = []
    # for tuan_start_time in tuan_start_time_list:
    #     start_time = tuan_start_time.text
    #     tuan_start_time_l.append(start_time)
    tuan_remain_l = []
    for tuan_remain in tuan_remain_list:
        remain_time = tuan_remain.text
        tuan_remain_l.append(remain_time)
    tuan_pic_l = []
    for tuan_pic in tuan_pic_list:
        #print(tuan_pic.get_attribute("outerHTML"))
        tuan_pic = tuan_pic.get_attribute("data-original")
        tuan_pic_l.append(tuan_pic)
    
    link_list = []
    link_list = read_previous_file()
    i = 0
    today_date = datetime.date.today().strftime('%m%d')
    past_date1 = (datetime.date.today() - datetime.timedelta(days=1)).strftime('%m%d')
    past_date2 = (datetime.date.today() - datetime.timedelta(days=2)).strftime('%m%d')

    for link in tuan_link_list:
        # if link not in link_list:
        if tuan_start_time_list[i] == today_date or tuan_start_time_list[i]==past_date1 or tuan_start_time_list[i]==past_date2:
            if link not in link_list:
                if tuan_remain_l[i] != "已结束":
                    temp = {
                        "link":tuan_link_list[i],
                        "name":tuan_name_l[i],
                        "start":tuan_start_time_list[i], 
                        "status":tuan_remain_l[i],
                        "leader":'@'+tuan_leader_l[i],
                        "pic":"<img data-original=\""+ tuan_pic_l[i] + "\" src=\"" + tuan_pic_l[i] + "\" style=\"display: block;\">"
                    }
                    result.append(temp)

        i+=1
    return result

def get_ongoing_tuan():
    # browser = webdriver.Chrome()
    chrome_options = Options()  
    #chrome_options.add_argument("--headless") 
    browser = webdriver.Chrome(chrome_options=chrome_options)
    results = []
    for query in [
        #command + '/'
       "&page=0",
       "&page=1",
       "&page=2",
       "&page=3",
       "&page=4",
       "&page=5"
    ]:
        results += get_all_tuan(browser, query)
        # get_all_tuan(browser,query)
        time.sleep(3)
    browser.close()
    #write post function
    #post_func(results)

    my_date = datetime.date.today().strftime('%m%d')
    nestedlist2csv(results,'result_' + my_date +'.csv')
    # write nested list of dict to csv

def read_previous_file():
    my_date_yesterday = (datetime.date.today() - datetime.timedelta(days=1)).strftime('_%m%d')
    my_date_yesterday2 = (datetime.date.today() - datetime.timedelta(days=2)).strftime('_%m%d')
    
    in_file = "result"+ my_date_yesterday+".csv"
    with open(in_file,'r') as in_f:
        csv_reader = csv.reader(in_f, delimiter=',')
        link_list = []

        for row in csv_reader:
            link_list.append(row[0])
    in_file2 = "result"+ my_date_yesterday2+".csv"
    with open(in_file2,'r') as in_f2:
        csv_reader = csv.reader(in_f2, delimiter=',')
        for row in csv_reader:
            link_list.append(row[0])
    return link_list


def nestedlist2csv(list, out_file):
    with open(out_file, 'w') as f:
        w = csv.writer(f)
        if list ==[]:
            return 0
        fieldnames=list[0].keys()  # solve the problem to automatically write the header
        w.writerow(fieldnames)
        for row in list:
            w.writerow(row.values())

def post_func(results):
    # browser = webdriver.Chrome()
    chrome_options = Options()  
    #chrome_options.add_argument("--headless") 
    browser = webdriver.Chrome(chrome_options=chrome_options)

    browser.get("http://www.lukou.com")
    browser.find_element_by_class_name("login").click()
    browser.find_element_by_id("email").send_keys("15652719062")
    browser.find_element_by_id ("password").send_keys("ryp1995510")
    browser.find_element_by_id("loginSubmit").click()
    time.sleep(3)
    browser.get("http://www.lukou.com/post/blog")
    time.sleep(1)
    title_element = browser.find_element_by_css_selector("#form > div > div > div.title > input")
    #today:my_date = datetime.date.today().strftime('_%m%d')
    title_element.send_keys(datetime.date.today().strftime('%m%d'))
    time.sleep(3)
    content_element = browser.find_element_by_css_selector("#form > div > div > div.simditor.simditor-mac > div.simditor-wrapper > div.simditor-body")
    for row in results:
        row_list = list(row.values())
        content_element.send_keys(row_list)
        content_element.send_keys('\n')
    #browser.find_element_by_css_selector("#form > div > div > div.action > div > button.active.publish").click()
    #browser.close()

get_ongoing_tuan()


