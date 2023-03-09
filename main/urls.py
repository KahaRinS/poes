from django.contrib import admin
from django.urls import path, include
from main.views import SensorView, RegionView, ResultView, MainView

urlpatterns = [
    path('sensors/', SensorView),
    path('regions/', RegionView),
    path('results/', ResultView),
    path('', MainView),
]
