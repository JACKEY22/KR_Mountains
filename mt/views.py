from django.shortcuts import render
import folium
from pymongo import MongoClient
from django.core.paginator import Paginator
import requests
from urllib import parse
from folium.plugins import MarkerCluster

# Create your views here.
#192.168.219.104
#192.168.0.136
def home(request):
    pass
    return render(request, 'mt/home.html')

def krmt(request):
    center = [37.541, 126.986]
    m = folium.Map(center, zoom_start=7)
    marker_cluster = MarkerCluster().add_to(m)

    with MongoClient('mongodb://192.168.0.136:27017') as client:
        db = client.mydb 
        mt_data_list = list(db.mountain.find({}))
        wt_data_list = list(db.weather.find({}))

        for mt_data, wt_data in zip(mt_data_list,wt_data_list):
            mt_address_temp = mt_data['mt_address']
            mt_address = mt_address_temp.split(" ")[0]
            if mt_address in mt_data['mt_address']:
                lat_lon = [mt_data['mt_lat'], mt_data['mt_lon']]
                pop_text = folium.Html(
                    f"<img src={mt_data['mt_img_path_preview']} width=300px; height=300px;><br>" +
                    f"<a href='detail/{mt_data['mt_num']}/' target='_blank'><b>Mountain : {mt_data['mt_name']}</a><br>" +
                    f"<b>Height : {mt_data['mt_height']}m<br>" +
                    f"<b>Current weather : {wt_data['mt_weather_main']} <br>Current temperature : {wt_data['temp']}°C" , script=True
                )
                pop_up = folium.Popup(pop_text)
                folium.Marker(lat_lon, popup=pop_up, tooltip=mt_data['mt_name']).add_to(marker_cluster)

    paginator = Paginator(mt_data_list,10)
    page =request.GET.get('page',1)
    page_data = paginator.get_page(page)

    m = m._repr_html_()
    return render(request, 'mt/krmt.html', context={'page_data':page_data, 'map':m})
    
def krmt_detail(request, mt_num):
    with MongoClient('mongodb://192.168.0.136:27017') as client:
        db = client.mydb 

        mt_data = db.mountain.find({"mt_num" : mt_num})[0]
        wt_data = db.weather.find({"mt_num" : mt_num})[0]
        acc_data = db.acc.find({"mt_num" : mt_num})[0]
        hp_data = db.hp.find({"mt_num" : mt_num})[0]
        pm_data = db.pm.find({"mt_num" : mt_num})[0] #lat lon

        lat_lon = [mt_data['mt_lat'], mt_data['mt_lon']]
        m = folium.Map(lat_lon, zoom_start=12)
        if acc_data['acc_name'] != "None":
            acc_lat_lon = [acc_data['acc_lat'], acc_data['acc_lon']]
            pop_text = folium.Html(
                f"Name : <a href='{acc_data['acc_link']}' target='_blanck'>{acc_data['acc_name']}</a><br>" +
                f"Address : {acc_data['acc_address']}<br>" +
                f"Phone : {acc_data['acc_phone']}<br>", script=True
            )
            pop_up = folium.Popup(pop_text)

            iframe = folium.IFrame(pop_text, width=350, height=100)
            pop_up = folium.Popup(iframe, max_width=650)
            folium.Marker(acc_lat_lon, popup=pop_up, tooltip=acc_data['acc_name'], icon=folium.Icon(color='gray',icon='home')).add_to(m)

        if hp_data['hp_name'] != "None": 
            hp_lat_lon = [hp_data['hp_lat'], hp_data['hp_lon']]
            pop_text = folium.Html(
                f"Name : <a href='{hp_data['hp_link']}' target='_blanck'>{hp_data['hp_name']}</a><br>" +
                f"Address : {hp_data['hp_address']}<br>" +
                f"Phone : {hp_data['hp_phone']}<br>", script=True
            )
            iframe = folium.IFrame(pop_text, width=350, height=100)
            pop_up = folium.Popup(iframe, max_width=650)
            folium.Marker(hp_lat_lon, popup=pop_up, tooltip=hp_data['hp_name'] ,icon=folium.Icon(color='red',icon='star')).add_to(m)

        if pm_data['pm_name'] != "None":   
            pm_lat_lon = [pm_data['pm_lat'], pm_data['pm_lon']]
            pop_text = folium.Html(
                f"Name : <a href='{pm_data['pm_link']}' target='_blanck'>{pm_data['pm_name']}</a><br>" +
                f"Address : {pm_data['pm_address']}<br>" +
                f"Phone : {pm_data['pm_phone']}<br>", script=True
            )
            iframe = folium.IFrame(pop_text, width=350, height=100)
            pop_up = folium.Popup(iframe, max_width=650)
            folium.Marker(pm_lat_lon, popup=pop_up, tooltip=pm_data['pm_name'] ,icon=folium.Icon(color='green')).add_to(m)

        

        pop_text = folium.Html(
                f"<img src={mt_data['mt_img_path_preview']} width=300px; height=300px;><br>" +
                f"<b>Mountain : {mt_data['mt_name']} <br>" +
                f"<b>Height : {mt_data['mt_height']}m <br>" +
                f"<b>Current weather : {wt_data['mt_weather_main']} <br> Current temperature : {wt_data['temp']}°C", script=True
            )
        pop_up = folium.Popup(pop_text)
        folium.Marker(lat_lon, popup=pop_up, tooltip=mt_data['mt_name']).add_to(m)
    

        folium.Circle(
        lat_lon,
        radius=5000,
        color='#ffffgg',
        fill_color='#fffggg',
        popup='10km'
        ).add_to(m)

        folium.Circle(lat_lon,
        radius=2500,
        color='#ffffgg',
        fill_color='#fffggg',
        popup='5km'
        ).add_to(m)
        
        m = m._repr_html_()
    return render(request, 'mt/krmt_detail.html', context={'map':m})

def krmt_detail_view(request, mt_num):
    with MongoClient('mongodb://192.168.0.136:27017') as client:
        db = client.mydb 
        data ={
                'mt_name' : db.mountain.find({"mt_num" : mt_num})[0]['mt_name'],
                'mt_address' : db.mountain.find({"mt_num" : mt_num})[0]['mt_address'],
                'mt_height': db.mountain.find({"mt_num" : mt_num})[0]['mt_height'],
                'mt_lat': db.mountain.find({"mt_num" : mt_num})[0]['mt_lat'],
                'mt_lon': db.mountain.find({"mt_num" : mt_num})[0]['mt_lon'],
                'mt_comment': db.mountain.find({"mt_num" : mt_num})[0]['mt_comment'],
                'mt_img_path': db.mountain.find({"mt_num" : mt_num})[0]['mt_img_path'],
                'sunrise' : db.weather.find({"mt_num" : mt_num})[0]['sunrise'],
                'sunset' : db.weather.find({"mt_num" : mt_num})[0]['sunset'],
                'wind_speed' : db.weather.find({"mt_num" : mt_num})[0]['wind_speed'],
                'wind_deg' : db.weather.find({"mt_num" : mt_num})[0]['wind_deg'],
                'weather_main' : db.weather.find({"mt_num" : mt_num})[0]['mt_weather_main'],
                'temp' : db.weather.find({"mt_num" : mt_num})[0]['temp']
              }   

    return render(request, 'mt/krmt_detail_view.html', context=data)


