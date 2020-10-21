import requests, json
import urllib
from selenium import webdriver
from selenium.webdriver.common.alert import Alert
import time

# UPP_AIS_TP_CD 공고유형코드 06 임대주택
# CNP_CD 지역코드 11 서울특별시 41 경기도 28 인천광역시

# UPP_AIS_TP_NM 공고유형명
# AIS_TP_CD_NM 공고세부유형명
# PAN_NM 공고명
# CNP_CD_NM 지역명
# DTL_URL 공고상세URL

# url = 'http://apis.data.go.kr/B552555/lhLeaseNoticeInfo/lhLeaseNoticeInfo?serviceKey=b1NZ2gr%2FbqGzGDHPOVvY9y6lARiQeJujooUewpFC708umNxQRcfgcKSuZIEcJU7Q6yLlyVGp0s6p4dCrEEzZnQ%3D%3D&PG_SZ=100&PAGE=1&UPP_AIS_TP_CD=06&PAN_SS=공고중'
# res = requests.get(url=url)
# data = json.loads(res.content)
# jdata = data[1]
# print(len(jdata['dsList']))

url = 'https://apply.lh.or.kr/LH/index.html#SIL::CLCC_SIL_0030:1010203'
driver = webdriver.Chrome(executable_path='../chromedriver')
driver.get(url = url)

driver.switch_to_window(driver.window_handles[0]) 

time.sleep(10)
driver.close()

time.sleep(2)