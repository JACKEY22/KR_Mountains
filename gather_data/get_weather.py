import requests
from bs4 import BeautifulSoup as bs
from urllib import parse

API_key = 'd9a33dfaa19a045b98d9e6f57ce733ba'
url = f'https://api.openweathermap.org/data/2.5/onecall?lon=127.304809447716&lat=36.1438091343544&units=metric&appid={API_key}'

res = requests.get(url).json()
print(res['current']['dt'])
print(res['current']['sunrise'])
print(res['current']['sunset'])
print(res['current']['temp'])
print(res['current']['pressure'])
print(res['current']['humidity'])
print(res['current']['wind_speed'])
print(res['current']['wind_deg'])
print(res['current']['weather'][0]['main'])
print(res['current']['weather'][0]['description'])

