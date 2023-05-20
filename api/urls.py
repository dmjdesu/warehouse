from django.urls import path, include
from api.views import *
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'history', ShoppingHistoryJson)

urlpatterns = router.urls
urlpatterns += [
    path('shoppinghistory-list/<str:fk1>',ShoppingHistoryJson.as_view({'get': 'list'}), name="shoppinghistory-list"),
]
