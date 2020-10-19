import requests
from pymongo import MongoClient
############################################
## openWeather - get weather info
############################################
def weather():
    with MongoClient('mongodb://192.168.0.136:27017') as client:
        db = client.mydb
        data_list = list(db.mountain.find({}))

        for data in data_list:
            data_temp ={}
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
            data_temp['mt_weather_main']=(res['current']['weather'][0]['main'])
            data_temp['mt_name']=(data['mt_name'])
            # print(res['current']['weather'][0]['description'])
            db.weather.insert(data_temp)
weather()
        #db.weather.update({'mt_name':data_temp['mt_name']},{'mt_weather_main': data_temp['mt_weather_main']}})