from django.shortcuts import render
import folium
from pymongo import MongoClient
from django.core.paginator import Paginator
import requests
# Create your views here.

def home(request):
    center = [37.541, 126.986]
    m = folium.Map(center, zoom_start=7)

    with MongoClient('mongodb://192.168.219.104:27017') as client:
        db = client.mydb 
        data_list = list(db.mountain.find({}))
        for data in data_list:
            lat_lon = [data['mt_lat'],data['mt_lon']]
            pop_text = folium.Html(
                f"<img src={data['mt_img_path']}><br>" +
                f"{data['mt_name']}<br>" +
                f"{data['mt_height']}<br>", script=True
            )
            pop_up = folium.Popup(pop_text, max_width=100)
            folium.Marker(lat_lon, popup=pop_up, tooltip=data['mt_name']).add_to(m)

        paginator = Paginator(data_list,10)
        page =request.GET.get('page',1)
        posts = paginator.get_page(page)

    m = m._repr_html_()
    return render(request, 'mt/home.html', context={'posts':posts, 'map':m})

def krmt(request):
    pass
    return render(request, 'mt/krmt.html')

def acc(request):
    pass
    return render(request, 'mt/acc.html')
    
    