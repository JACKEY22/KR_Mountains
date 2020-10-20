from django.shortcuts import render
import folium
from pymongo import MongoClient
from django.core.paginator import Paginator
import requests
from urllib import parse
# Create your views here.
#192.168.219.104
#192.168.0.136
def home(request):
    pass
    return render(request, 'mt/home.html')

def krmt(request):
    center = [37.541, 126.986]
    m = folium.Map(center, zoom_start=7)

    with MongoClient('mongodb://192.168.219.104:27017') as client:
        db = client.mydb 
        mt_data_list = list(db.mountain.find({}))
        wt_data_list = list(db.weather.find({}))

        for mt_data, wt_data in zip(mt_data_list,wt_data_list):
            lat_lon = [mt_data['mt_lat'], mt_data['mt_lon']]
            pop_text = folium.Html(
                f"<img src={mt_data['mt_img_path_preview']} width=300px; height=300px;><br>" +
                f"<b>Mountain : {mt_data['mt_name']}<br>" +
                f"<b>Height : {mt_data['mt_height']}m<br>" +
                f"<b>Current weather : {wt_data['mt_weather_main']} <br>Current temperature : {wt_data['temp']}°C", script=True
            )
            pop_up = folium.Popup(pop_text)
            folium.Marker(lat_lon, popup=pop_up, tooltip=mt_data['mt_name']).add_to(m)

    paginator = Paginator(mt_data_list,10)
    page =request.GET.get('page',1)
    page_data = paginator.get_page(page)

    m = m._repr_html_()
    return render(request, 'mt/krmt.html', context={'page_data':page_data, 'map':m})
    
def krmt_detail(request,mt_num):
    with MongoClient('mongodb://192.168.219.104:27017') as client:
        db = client.mydb 

        mt_data = db.mountain.find({"mt_num" : mt_num})[0]
        wt_data = db.weather.find({"mt_num" : mt_num})[0]
        acc_data = db.acc.find({"mt_num" : mt_num})[0]
        hp_data = db.hp.find({"mt_num" : mt_num})[0]
        pm_data = db.pm.find({"mt_num" : mt_num})[0] #lat lon

        lat_lon = [mt_data['mt_lat'], mt_data['mt_lon']]
        m = folium.Map(lat_lon, zoom_start=12)
        if acc_data['acc_name'] != "None":
            acc_lat_lon = [mt_data['mt_lat'], mt_data['mt_lon']]
            folium.Marker(acc_lat_lon, tooltip=acc_data['acc_name'], icon=folium.Icon(color='gray',icon='home')).add_to(m)

        if hp_data['hp_name'] != "None": 
            hp_lat_lon = [hp_data['hp_lat'], hp_data['hp_lon']]
            folium.Marker(hp_lat_lon, tooltip=hp_data['hp_name'] ,icon=folium.Icon(color='red',icon='star')).add_to(m)

        if pm_data['pm_name'] != "None":   
            pm_lat_lon = [pm_data['pm_lat'], pm_data['pm_lon']]
            folium.Marker(pm_lat_lon, tooltip=pm_data['pm_name'] ,icon=folium.Icon(color='green')).add_to(m)

        

        pop_text = folium.Html(
                f"<img src={mt_data['mt_img_path_preview']} width=300px; height=300px;><br>" +
                f"<b>Mountain : {mt_data['mt_name']} <br>" +
                f"<b>Height : {mt_data['mt_height']}m< br>" +
                f"<b>Current weather : {wt_data['mt_weather_main']} <br> Current temperature : {wt_data['temp']}°C", script=True
            )
        pop_up = folium.Popup(pop_text)
        folium.Marker(lat_lon, popup=pop_up, tooltip=mt_data['mt_name']).add_to(m)
         # color
        
        
        
        m = m._repr_html_()
    return render(request, 'mt/krmt_detail.html',context={'map':m})


def acc(request):
    center = [37.541, 126.986]
    m = folium.Map(center, zoom_start=7)

    with MongoClient('mongodb://192.168.219.104:27017') as client:
        db = client.mydb 
        data_list = list(db.mountain.find({}))
        data_list2 = list(db.weather.find({}))
        data_list3 = list(db.acc.find({}))
        for data,data2 in zip(data_list,data_list2):
            lat_lon = [data['mt_lat'],data['mt_lon']]
            pop_text = folium.Html(
                f"<img src={data['mt_img_path_preview']} width=300px; height=300px;><br>" +
                f"<b>Mountain : {data['mt_name']}<br>" +
                f"<b>Height : {data['mt_height']}m<br>" +
                f"<b>Current weather : {data2['mt_weather_main']} <br>Current temperature : {data2['temp']}°C", script=True
            )
            pop_up = folium.Popup(pop_text)
            folium.Marker(lat_lon, popup=pop_up, tooltip=data['mt_name']).add_to(m)

        for data3 in data_list3:
            lat_lon2 = [data3['mt_acc_lat'],data3['mt_acc_lon']]
            pop_text = folium.Html(
                f"Name : <a href='{data3['mt_acc_link']}' target='_blanck'>{data3['mt_acc_name']}</a><br>" +
                f"Address : {data3['mt_acc_address']}<br>" +
                f"Phone : {data3['mt_acc_phone']}<br>", script=True
            )
            pop_up = folium.Popup(pop_text)

            iframe = folium.IFrame(pop_text, width=350, height=100)
            pop_up = folium.Popup(iframe, max_width=650)
            folium.Marker(lat_lon2, popup=pop_up, tooltip=data3['mt_acc_name'], icon=folium.Icon(color='gray',icon = 'home')).add_to(m)

                
        paginator = Paginator(data_list3,10)
        page =request.GET.get('page',1)
        page_data = paginator.get_page(page)

    m = m._repr_html_()
    return render(request, 'mt/acc.html',context={'page_data':page_data, 'map':m})