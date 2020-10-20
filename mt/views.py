from django.shortcuts import render
import folium
from pymongo import MongoClient
from django.core.paginator import Paginator
import requests
# Create your views here.

def home(request):
    pass
    return render(request, 'mt/home.html')

def krmt(request):
    center = [37.541, 126.986]
    m = folium.Map(center, zoom_start=7)

    with MongoClient('mongodb://192.168.219.104') as client:
        db = client.mydb 
        data_list = list(db.mountain.find({}))
        data_list2 = list(db.weather.find({}))
        for data,data2 in zip(data_list,data_list2):
            lat_lon = [data['mt_lat'],data['mt_lon']]
            pop_text = folium.Html(
                f"<img src={data['mt_img_path_preview']} width=300px; height=300px;><br>" +
                f"{data['mt_name']}<br>" +
                f"{data['mt_height']}m<br>" +
                f"{data2['mt_weather_main']}", script=True
            )
            pop_up = folium.Popup(pop_text)
            folium.Marker(lat_lon, popup=pop_up, tooltip=data['mt_name']).add_to(m)

        paginator = Paginator(data_list,10)
        page =request.GET.get('page',1)
        page_data = paginator.get_page(page)

    m = m._repr_html_()
    return render(request, 'mt/krmt.html', context={'page_data':page_data, 'map':m})

def acc(request):
    center = [37.541, 126.986]
    m = folium.Map(center, zoom_start=7)

    with MongoClient('mongodb://192.168.219.104:27017') as client:
        db = client.mydb 
        data_list = list(db.mountain.find({}))
        data_list2 = list(db.weather.find({}))
        for data,data2 in zip(data_list,data_list2):
            lat_lon = [data['mt_lat'],data['mt_lon']]
            pop_text = folium.Html(
                f"<img src={data['mt_img_path_preview']} width=300px; height=300px;><br>" +
                f"{data['mt_name']}<br>" +
                f"{data['mt_height']}m<br>" +
                f"{data2['mt_weather_main']}", script=True
            )
            pop_up = folium.Popup(pop_text)
            folium.Marker(lat_lon, popup=pop_up, tooltip=data['mt_name']).add_to(m)
            
            if data['mt_acc_name'] != "Null":
                lat_lon2 = [data['mt_acc_lat'],data['mt_acc_lon']]
                pop_text = folium.Html(
                    f"<a href='{data['mt_acc_link']}' target='_blanck'>{data['mt_acc_name']}</a><br>" +
                    f"{data['mt_acc_address']}<br>" +
                    f"{data['mt_acc_phone']}<br>", script=True
                )
                pop_up = folium.Popup(pop_text)

                iframe = folium.IFrame(pop_text, width=300, height=100)
                pop_up = folium.Popup(iframe, max_width=650)
                folium.Marker(lat_lon2, popup=pop_up, tooltip=data['mt_acc_name'], icon=folium.Icon(color='gray',icon = 'home')).add_to(m)

                
        paginator = Paginator(data_list,10)
        page =request.GET.get('page',1)
        page_data = paginator.get_page(page)

    m = m._repr_html_()
    return render(request, 'mt/acc.html',context={'page_data':page_data, 'map':m})
    
def krmt_detail(request):
    with MongoClient('mongodb://192.168.219.104:27017') as client:
        data_list = list(db.mountain.find({}))
        data_list2 = list(db.weather.find({}))
    #     for data,data2 in zip(data_list,data_list2):
    # pass
    return render(request, 'mt/krmt_detail.html',context={'data_list':data_list, 'data_list2':data_list2})