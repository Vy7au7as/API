from django.urls import path
from . import views
from django.urls import path
from .views import search, download_csv


urlpatterns = [
    path('', views.search, name='search'),
    path('download-csv/', views.download_csv, name='download_csv'),
    path('details/', views.details, name='details'),



]
