from django.shortcuts import render
from .serializers import ShoppingHistorySerializer
from stock.models import *
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from pprint import pprint

class ShoppingJson(ModelViewSet):
    serializer_class = ShoppingHistorySerializer
    queryset = ShoppingHistory.objects.all()

    def create(self, request, *args, **kwargs):
        pprint(request.data)
        return Response(status=status.HTTP_201_CREATED)
