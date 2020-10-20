import requests, json
import urllib

url = 'http://apis.data.go.kr/B552555/lhLeaseNoticeInfo/lhLeaseNoticeInfo?serviceKey=b1NZ2gr%2FbqGzGDHPOVvY9y6lARiQeJujooUewpFC708umNxQRcfgcKSuZIEcJU7Q6yLlyVGp0s6p4dCrEEzZnQ%3D%3D&PG_SZ=10&PAGE=1'
res = requests.get(url=url)
data = json.loads(res.content)
jdata = data[1]
#print(jdata.keys())
print(jdata['dsList'])

print(jdata['dsList'][0]['UPP_AIS_TP_NM'])
# ,jdata['dsList'][0]['AIS_TP_CD_NM']
# ,jdata['dsList'][0]['PAN_NM']
# ,jdata['dsList'][0]['CNP_CD_NM']
# ,jdata['dsList'][0]['PAN_SS']
# ,jdata['dsList'][0]['DTL_URL'])