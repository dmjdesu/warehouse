from django.urls import path
from .views import *

urlpatterns = [
    path('admin/stock/shoppinghistory/add/', ShoppingHistoryView.as_view(), name='shopping_history'),
    path('admin/stock/shoppinghistoryproxy/add/', RedirectToShoppingHistoryView.as_view(), name='rredirect_shopping_history'),
    path('predict_purchase/', ShoppingPredictionView.as_view(), name='predict_purchase'),
]
