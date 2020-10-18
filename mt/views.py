from django.shortcuts import render
import folium
# Create your views here.

def home(request):
    return render(request, 'mt/home.html')

def krmt(request):
    pass
    return render(request, 'mt/krmt.html')

def acc(request):
    pass
    return render(request, 'mt/acc.html')
    
    