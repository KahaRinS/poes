from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from main.views import SensorView, RegionView, ResultView
from users.views import UserViewSet
router = routers.SimpleRouter()
router.register(r'user', UserViewSet, basename='user')

urlpatterns = router.urls
