from django.shortcuts import render
from stock.models import *
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from pprint import pprint
from decimal import Decimal
from api.models import *
from api.serializers import *

class ShoppingHistoryJson(ModelViewSet):
    serializer_class = ShoppingHistorySerializer
    queryset = ShoppingHistory.objects.all()

    def create(self, request, *args, **kwargs):
        material = Material.objects.get(id=request.POST["material_id"])
        werehouse = Warehouse.objects.get_or_create(material=material)

        if request.POST["target_name"] == "warehouse" :
            try:
                WarehouseHistory.objects.create(
                    target_name = request.POST["target_name"],
                    value=round(Decimal(request.POST["num"]) * material.value,4),
                    num=(Decimal(request.POST["num"])),
                    material_name=material.name,
                    material_item_name=material.item.name,
                    material_unit=material.unit,
                    date=request.POST["date"],
                    is_send=False
                )
                werehouse[0].num += Decimal(request.POST["num"])
                werehouse[0].save()
                return Response(status=status.HTTP_200_OK)
            except Exception:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            
        else:
            try:
                history = ShoppingHistory.objects.create(
                    target_name = request.POST["target_name"],
                    value=round(Decimal(request.POST["num"]) * material.value,4),
                    num=(Decimal(request.POST["num"])),
                    material_name=material.name,
                    material_item_name=material.item.name,
                    material_parent_category_name=material.item.parent.name,
                    material_unit=material.unit,
                    date=request.POST["date"],
                    is_send=False
                ) 
                werehouse[0].num -= Decimal(request.POST["num"])
                werehouse[0].save()
                return Response({'id': history.id}, status=status.HTTP_200_OK)
            except Exception:            
                return Response(status=status.HTTP_400_BAD_REQUEST)
            
            

        
