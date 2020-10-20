import requests
from pymongo import MongoClient
############################################
## openWeather - get weather info
############################################
def weather():
    with MongoClient('mongodb://192.168.219.104:27017') as client:
        db = client.mydb
        data_list = list(db.mountain.find({}))

        for data in data_list:
            data_temp ={}
            API_key = 'd9a33dfaa19a045b98d9e6f57ce733ba'
            url = f'https://api.openweathermap.org/data/2.5/onecall?lat={data["mt_lat"]}&lon={data["mt_lon"]}&units=metric&appid={API_key}'
            res = requests.get(url).json()

            data_temp['mt_name']=data['mt_name']
            data_temp['mt_num']=data['mt_num']
            data_temp['mt_weather_main']=res['current']['weather'][0]['main']
            data_temp['temp']= res['current']['temp']
            data_temp['sunrise']=res['current']['sunrise']
            data_temp['sunset']=res['current']['sunset']
            data_temp['wind_speed']=res['current']['wind_speed']
            data_temp['wind_deg']=res['current']['wind_deg']

            #db.weather.insert(data_temp)
            db.weather.update({'mt_name':data_temp['mt_name']},{ '$set':{'mt_num':data_temp['mt_num'],'mt_weather_main': data_temp['mt_weather_main'],'temp': data_temp['temp'],'sunrise':data_temp['sunrise'],'sunset':data_temp['sunset'],'wind_speed':data_temp['wind_speed'],'wind_deg':data_temp['wind_deg']}})
            # { '$set':{data_temp}}})
weather()
        