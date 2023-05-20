from django.shortcuts import redirect
from django.views import View
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
    queryset = ShoppingHistory.objects.order_by("-updated_at")

    def get_queryset(self):
        queryset = None

        if self.kwargs.get('fk1'):
            queryset = ShoppingHistory.objects.filter(target_name=self.kwargs.get('fk1'))
        else:
            queryset = ShoppingHistory.objects.order_by("-updated_at")

        return queryset

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
                gst = 0
                pst = 0
                drink_gst = 0
                bottle_deposit = 0
                recycle_fee = 0
                if material.is_gst : gst = round(Decimal(request.POST["num"]) * material.value * Decimal(0.05),4)
                if material.is_pst : pst = round(Decimal(request.POST["num"]) * material.value * Decimal(0.07),4)
                if material.is_drink_gst : drink_gst = round(Decimal(request.POST["num"]) * material.value * Decimal(0.05),4)
                if material.is_bottle_deposit : bottle_deposit = material.bottle_num * 0.1
                if material.is_recycle_fee : recycle_fee = material.bottle_num * 0.02
                history = ShoppingHistory.objects.create(
                    target_name = request.POST["target_name"],
                    value=round(Decimal(request.POST["num"]) * material.value,4),
                    gst= gst,
                    pst= pst,
                    bottle_deposit=bottle_deposit,
                    recycle_fee=recycle_fee,
                    drink_gst=drink_gst,
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