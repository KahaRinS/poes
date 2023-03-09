from django.contrib import admin
from django.urls import path, include
from main.views import SensorView, RegionView, ResultView

urlpatterns = [
    path('register/', SensorView),
    path('login/', RegionView),
]
