import requests, json
import urllib
from selenium import webdriver
from selenium.webdriver.common.alert import Alert
from bs4 import BeautifulSoup as bs
import time

# UPP_AIS_TP_CD 공고유형코드 06 임대주택
# CNP_CD 지역코드 11 서울특별시 41 경기도 28 인천광역시

# UPP_AIS_TP_NM 공고유형명
# AIS_TP_CD_NM 공고세부유형명
# PAN_NM 공고명
# CNP_CD_NM 지역명
# DTL_URL 공고상세URL

anc_list = []
url = 'http://apis.data.go.kr/B552555/lhLeaseNoticeInfo/lhLeaseNoticeInfo?serviceKey=b1NZ2gr%2FbqGzGDHPOVvY9y6lARiQeJujooUewpFC708umNxQRcfgcKSuZIEcJU7Q6yLlyVGp0s6p4dCrEEzZnQ%3D%3D&PG_SZ=100&PAGE=1&UPP_AIS_TP_CD=06&PAN_SS=공고중'
res = requests.get(url=url)
data = json.loads(res.content)
jdata = data[1]
for i in range(0,len(jdata['dsList'])):   
    anc_list.append(jdata['dsList'][i]['PAN_NM'])
print(anc_list)

