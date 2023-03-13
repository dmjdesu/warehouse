from django.urls import path
from . import views

urlpatterns = [
    path('shopping_history', views.ShoppingHistoryView.as_view(), name='shopping_history'),
    # path('purchase_history', views.PurchaseHistoryView.as_view(), name='stock'),
]
