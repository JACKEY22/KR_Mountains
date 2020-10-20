from selenium import webdriver
from selenium.webdriver.common.keys import Keys as keys
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as bs 
from pymongo import MongoClient
import json
import requests

data = {
        "mt_name":[],
        "mt_height":[],
        "mt_lat":[],
        "mt_lon":[],
        "mt_comment":[],
        'mt_address' : [],
        "mt_img_path" :[],
        'mt_img_path_preview':[]
       }   

options = Options()
options.add_argument('--headless')
driver = webdriver.Chrome(executable_path="../chromedriver", chrome_options=options)
driver.get(url="http://bac.blackyak.com/html/challenge/ChallengeVisitList.asp?CaProgram_key=114")

soup = bs(driver.page_source, 'lxml')  
data['mt_name'] = [mt_name.text.strip() for mt_name in soup.select('.text span:nth-child(1)')]
data['mt_lat'] = [mt_x.text.strip().split(',')[0] for mt_x in soup.select('.text a')]
data['mt_lon'] = [mt_y.text.strip().split(',')[1] for mt_y in soup.select('.text a')]
data['mt_img_path'] = [mt_img_path['src'] for mt_img_path in soup.select('div.img img')]

detail_button = driver.find_elements_by_css_selector('button.btnType06_03')
for view in detail_button:
 
    driver.execute_script("arguments[0].click();", view)
    last_tab = driver.window_handles[-1]
    first_tab = driver.window_handles[0]
    driver.switch_to.window(window_name=last_tab)
    
    soup = bs(driver.page_source,'lxml')
    mt_address = soup.select_one('#contents > div > div.secTion.a1 > div.visitArea > div > p > em').text
    mt_comment = soup.select_one('div:nth-child(2) > div.right > p.visitText').text
    mt_height = soup.select_one('div:nth-child(3) > div.right > p.visitText').text.split(":")[3].strip()
    mt_img_path_preview = soup.select_one('#contents > div > div.secTion.a1 > div:nth-child(2) > div.left > div > div > ul > li > img')['src']

    data['mt_address'].append(mt_address)
    data["mt_comment"].append(mt_comment)
    data["mt_height"].append(mt_height)
    data['mt_img_path_preview'].append(mt_img_path_preview)
 

    driver.close()   
    driver.switch_to.window(window_name=first_tab)
    
driver.quit()

# with MongoClient('mongodb://192.168.0.136:27017') as client:
#     db = client.mydb
#     for i in range(1,101):
#         mt_data = {
#                     "mt_num":i,
#                     "mt_name":data['mt_name'][i-1],
#                     "mt_height":data['mt_height'][i-1],
#                     "mt_lat":data['mt_lat'][i-1],
#                     "mt_lon":data['mt_lon'][i-1],
#                     "mt_comment":data['mt_comment'][i-1],
#                     "mt_address":data['mt_address'][i-1],
#                     "mt_img_path":data['mt_img_path'][i-1],
#                     "mt_img_path_preview":data['mt_img_path_preview'][i-1]
#                   }
#         db.mountain.insert(mt_data)

######################################
## kakaoAPI - get mt_acc_info
######################################
with MongoClient('mongodb://192.168.0.136:27017') as client:

    db = client.mydb
    acc_data = {
            "mt_id":[],
            "acc_address":[],
            "acc_phone":[],
            "acc_lon":[],
            "acc_lat":[],
            "acc_link":[]
            }  
    hp_data = {
            "mt_id":[],
            "hp_address":[],
            "hp_phone":[],
            "hp_lon":[],
            "hp_lat":[],
            "hp_link":[]
            }  
    pm_data = {
            "mt_id":[],
            "pm_address":[],
            "pm_phone":[],
            "pm_lon":[],
            "pm_lat":[],
            "pm_link":[]
            }  

    code_list = ['AD5','HP8','PM9']
    i = 0
    for code in code_list:
        for mt_name_temp in data['mt_name']:
            i = i+1
            if "(" in mt_name:
                mt_name = mt_name_temp.split("(")[0]
            else:
                mt_name = mt_name_temp
                
            url = f'https://dapi.kakao.com/v2/local/search/keyword.json?query={mt_name}&category_group_code={code}'
            headers = {"Authorization": "KakaoAK 9d8f1d66de33937b1015fb76a800fee7"}
            res = requests.get(url, headers = headers).json()
            
            if code == 'AD5':
                acc_data['mt_num'].append(i)
                acc_data['acc_address'].append(res['documents'][0]['address_name'])
                acc_data['acc_phone'].append(res['documents'][0]['phone'])
                acc_data['acc_lon'].append(res['documents'][0]['x'])
                acc_data['acc_lat'].append(res['documents'][0]['y'])
                acc_data['acc_link'].append(res['documents'][0]['place_url'])
                db.acc.insert(acc_data)
                
            elif code == 'HP8':
                acc_data['mt_num'].append(i)
                hp_data['hp_address'].append(res['documents'][0]['address_name'])
                hp_data['hp_phone'].append(res['documents'][0]['phone'])
                hp_data['hp_lon'].append(res['documents'][0]['x'])
                hp_data['hp_lat'].append(res['documents'][0]['y'])
                hp_data['hp_link'].append(res['documents'][0]['place_url'])
                db.hp.insert(hp_data)

            elif code == 'PM9':
                acc_data['mt_num'].append(i)
                pm_data['pm_address'].append(res['documents'][0]['address_name'])
                pm_data['pm_phone'].append(res['documents'][0]['phone'])
                pm_data['pm_lon'].append(res['documents'][0]['x'])
                pm_data['pm_lat'].append(res['documents'][0]['y'])
                pm_data['pm_link'].append(res['documents'][0]['place_url'])
                db.pm.insert(pm_data)
        
        
            