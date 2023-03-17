from django.urls import path
from . import views

urlpatterns = [
    path('admin/stock/shoppinghistory/add/', views.ShoppingHistoryView.as_view(), name='shopping_history'),
    path('admin/stock/shoppinghistoryproxy/add/', views.ShoppingHistoryView.as_view(), name='shopping_history'),
    # path('purchase_history', views.PurchaseHistoryView.as_view(), name='stock'),
]
