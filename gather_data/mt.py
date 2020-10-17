from selenium import webdriver
from selenium.webdriver.common.keys import Keys as keys
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as bs 
from pymongo import MongoClient
import time, datetime
import json
import requests
import urllib


data = {"mt_name_list":[],
        "mt_height":[],
        "mt_x":[],
        "mt_y":[],
        "mt_acc_address":[],
        "mt_acc_phone" :[],
        "mt_acc_name":[],
        "mt_acc_link":[],
        "mt_acc_x" :[],
        "mt_acc_y":[],
        "img_src" :[]
        }

###################################
##driver
###################################
options = Options()
options.add_argument('--headless')

driver = webdriver.Chrome(executable_path="../chromedriver", chrome_options=options)
driver.get(url="http://www.forest.go.kr/kfsweb/kfi/kfs/foreston/main/contents/FmmntSrch/selectFmmntSrchList.do?mn=NKFS_03_01_12")
driver.find_element_by_xpath('//*[@id="mntUnit"]/option[5]').click()
driver.find_element_by_xpath('//*[@id="txt"]/form/div[2]/div[2]/button').click()
driver.implicitly_wait(10)

soup = bs(driver.page_source, features='lxml')
div = soup.select('div.list_info')

for i in div:
    mt_height = i.li.select("span")[1].text
    mt_name_temp = i.strong.text
    if "(" in mt_name_temp:
        mt_name = mt_name_temp.split("(")[0]
    else:
        mt_name = mt_name_temp
    data['mt_name_list'].append(mt_name)
    data['mt_height'].append(mt_height)

for mt_name in data['mt_name_list']:

    keyword = f'{mt_name}'
    url = f'https://dapi.kakao.com/v2/local/search/keyword.json?query={keyword}'
    headers = {"Authorization": "KakaoAK 9d8f1d66de33937b1015fb76a800fee7"}
    res = requests.get(url, headers = headers).json()

    mt_x = res['documents'][1]['x']
    mt_y = res['documents'][1]['y']
    data['mt_x'].append(mt_x)
    data['mt_y'].append(mt_y)

    url2 = f'https://dapi.kakao.com/v2/local/search/keyword.json?query={keyword}&category_group_code=AD5'
    headers = {"Authorization": "KakaoAK 9d8f1d66de33937b1015fb76a800fee7"}
    res = requests.get(url2, headers = headers).json()

    if len(res['documents']) >= 1:
        mt_acc_address = res['documents'][0]['address_name']
        mt_acc_phone =res['documents'][0]['phone']
        mt_acc_name = res['documents'][0]['place_name']
        mt_acc_link = res['documents'][0]['place_url']
        mt_acc_x = res['documents'][0]['x']
        mt_acc_y = res['documents'][0]['y']
    else:
        mt_acc_address = "Null"
        mt_acc_phone = "Null"
        mt_acc_name = "Null"
        mt_acc_link = "Null"
        mt_acc_x = "Null"
        mt_acc_y = "Null"
    data['mt_acc_address'].append(mt_acc_address)
    data['mt_acc_phone'].append(mt_acc_phone)
    data['mt_acc_name'].append(mt_acc_name)
    data['mt_acc_link'].append(mt_acc_link)
    data['mt_acc_x'].append(mt_acc_x)
    data['mt_acc_y'].append(mt_acc_y)

with MongoClient('mongodb://192.168.219.104:27017') as client:
    db = client.mydb
    for i in range(0,len(data['mt_name_list'])):
        data2 = {"mt_name_list":data['mt_name_list'][i],
                "mt_height":data['mt_height'][i],
                "mt_x":data['mt_x'][i],
                "mt_y":data['mt_y'][i],
                "mt_acc_address":data['mt_acc_address'][i],
                "mt_acc_phone" :data['mt_acc_phone'][i],
                "mt_acc_name":data['mt_acc_name'][i],
                "mt_acc_link":data['mt_acc_link'][i],
                "mt_acc_x" :data['mt_acc_x'][i],
                "mt_acc_y":data['mt_acc_y'][i]
            }
        db.mountain.insert(data2)

imgs = driver.find_elements_by_css_selector('.autosize')
for img in imgs:
    src = img.get_attribute("src")

    urllib.request.urlretrieve(src , f'static/imgs/{mt_name}.jpg')     

driver.quit()

#weather 
#img
#comment

#folium
#list 
#paging 

#bootstrap








        





