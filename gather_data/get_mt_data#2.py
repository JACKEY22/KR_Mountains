from selenium import webdriver
from selenium.webdriver.common.keys import Keys as keys
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as bs 
from pymongo import MongoClient
import time, datetime
import json
import requests
import urllib


data = {"mt_name":[],
        "mt_height":[],
        "mt_lat":[],
        "mt_lon":[],
        "mt_comment":[],
        "mt_img_path" :[],

        "mt_acc_address":[],
        "mt_acc_phone" :[],
        "mt_acc_name":[],
        "mt_acc_link":[],
        "mt_acc_lat" :[],
        "mt_acc_lon":[]
        }

options = Options()
options.add_argument('--headless')

driver = webdriver.Chrome(executable_path="../chromedriver", chrome_options=options)
driver.get(url="http://bac.blackyak.com/html/challenge/ChallengeVisitList.asp?CaProgram_key=114")
######################################
## selemium,bs - get mt_name,x,y,img_path
######################################
soup = bs(driver.page_source, 'lxml')
data['mt_name'] = [mt_name.text.strip() for mt_name in soup.select('.text span:nth-child(1)')]
data['mt_lat'] = [mt_x.text.strip().split(',')[0] for mt_x in soup.select('.text a')]
data['mt_lon'] = [mt_y.text.strip().split(',')[1] for mt_y in soup.select('.text a')]
data['mt_img_path'] = [mt_img_path['src'] for mt_img_path in soup.select('div.img img')]
#####################################
## selenium,bs - get mt_height
#####################################
detail_button = driver.find_elements_by_css_selector('button.btnType06_03')

for view in detail_button:
    
    driver.execute_script("arguments[0].click();", view)
    last_tab = driver.window_handles[-1]
    first_tab = driver.window_handles[0]
    driver.switch_to.window(window_name=last_tab)
    soup = bs(driver.page_source,'lxml')

    mt_comment_temp = soup.select_one('div:nth-child(2) > div.right > p.visitText').text
    if "." in mt_comment_temp:
        mt_comment = mt_comment_temp.split(".")[0]
    else:
        mt_comment = mt_comment_temp

    mt_height = soup.select_one('div:nth-child(3) > div.right > p.visitText').text.split(":")[3].strip()
    data["mt_comment"].append(mt_comment)
    data["mt_height"].append(mt_height)


    driver.close()   
    driver.switch_to.window(window_name=first_tab)
    
driver.quit()
######################################
## kakaoAPI - get mt_acc_info
######################################
for mt_name in data['mt_name']:
    url = f'https://dapi.kakao.com/v2/local/search/keyword.json?query={mt_name}&category_group_code=AD5'
    headers = {"Authorization": "KakaoAK 9d8f1d66de33937b1015fb76a800fee7"}
    res = requests.get(url, headers = headers).json()

    if len(res['documents']) >= 1:
        mt_acc_address = res['documents'][0]['address_name']
        mt_acc_phone =res['documents'][0]['phone']
        mt_acc_name = res['documents'][0]['place_name']
        mt_acc_link = res['documents'][0]['place_url']
        mt_acc_lon = res['documents'][0]['x']
        mt_acc_lat = res['documents'][0]['y']
    else:
        mt_acc_address = "Null"
        mt_acc_phone = "Null"
        mt_acc_name = "Null"
        mt_acc_link = "Null"
        mt_acc_lon = "Null"
        mt_acc_lat = "Null"
    data['mt_acc_address'].append(mt_acc_address)
    data['mt_acc_phone'].append(mt_acc_phone)
    data['mt_acc_name'].append(mt_acc_name)
    data['mt_acc_link'].append(mt_acc_link)
    data['mt_acc_lon'].append(mt_acc_lon)
    data['mt_acc_lat'].append(mt_acc_lat)  
###########################################
## pymongo - insert data
###########################################
with MongoClient('mongodb://192.168.0.136:27017') as client:
    db = client.mydb
    for i in range(0,len(data['mt_name'])):
        data2 = {"mt_name":data['mt_name'][i],
                "mt_height":data['mt_height'][i],
                "mt_lat":data['mt_lat'][i],
                "mt_lon":data['mt_lon'][i],
                "mt_comment":data['mt_comment'][i],
                "mt_img_path":data['mt_img_path'][i],
                "mt_acc_address":data['mt_acc_address'][i],
                "mt_acc_phone" :data['mt_acc_phone'][i],
                "mt_acc_name":data['mt_acc_name'][i],
                "mt_acc_link":data['mt_acc_link'][i],
                "mt_acc_lat" :data['mt_acc_lat'][i],
                "mt_acc_lon":data['mt_acc_lon'][i]
            }
    db.mountain.insert(data2)


#folium - django
#list 
#paging 
#bootstrap








        





