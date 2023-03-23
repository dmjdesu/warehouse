from django.urls import path, include
from api.views import *
from rest_framework import routers

router = routers.DefaultRouter()

router.register(r'shopping', ShoppingJson)

urlpatterns = router.urls

