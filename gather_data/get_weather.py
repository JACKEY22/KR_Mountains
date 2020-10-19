import requests
from pymongo import MongoClient
############################################
## openWeather - get weather info
############################################
with MongoClient('mongodb://192.168.0.136:27017') as client:
    db = client.mydb
    data_list = list(db.mountain.find({}))
    data_temp ={'mt_name':[],
           'mt_weather_main':[]
    }
    for data in data_list:
        API_key = 'd9a33dfaa19a045b98d9e6f57ce733ba'
        url = f'https://api.openweathermap.org/data/2.5/onecall?lat={data["mt_lat"]}&lon={data["mt_lon"]}&units=metric&appid={API_key}'
        res = requests.get(url).json()
        # print(res['current']['dt'])
        # print(res['current']['sunrise'])
        # print(res['current']['sunset'])
        # print(res['current']['temp'])
        # print(res['current']['pressure'])
        # print(res['current']['humidity'])
        # print(res['current']['wind_speed'])
        # print(res['current']['wind_deg'])
        data_temp['mt_weather_main'].append(res['current']['weather'][0]['main'])
        data_temp['mt_name'].append(data['mt_name'])
        # print(res['current']['weather'][0]['description'])
    db.weather.insert(data_temp)
    #db.weather.update({'mt_name':data_temp['mt_name']},{'mt_weather_main': data_temp['mt_weather_main']}})