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

class ParentCategoryJson(ModelViewSet):
    serializer_class = ParentCategorySerializer
    queryset = ParentCategory.objects.order_by("-name").prefetch_related('item_set')

    def get_queryset(self):
        return ParentCategory.objects.order_by("-name").prefetch_related('item_set')
    
    def get_serializer_context(self):
        """
        Overriding the default method to add the 'requested_date' to the serializer context.
        """
        context = super().get_serializer_context()

        requested_date = self.request.GET.get('date')  # Get date from query parameter
        if requested_date:
            requested_date = datetime.strptime(requested_date, "%Y-%m-%d").date()  # Convert to datetime object
            context['requested_date'] = requested_date

        requested_date = self.request.GET.get('target_name')  # Get date from query parameter
        if requested_date:
            context['target_name'] = requested_date

        return context

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
        material = Material.objects.get(id=request.data["material_id"])
        werehouse = Warehouse.objects.get_or_create(material=material)

        datetime_object = datetime.strptime(request.data["date"], "%Y-%m-%d")
        formatted_date = datetime_object.strftime("%Y-%m-%d")

        if request.data["target_name"] == "warehouse" :
            WarehouseHistory.objects.create(
                target_name = request.data["target_name"],
                value=round(Decimal(request.data["num"]) * material.value,4),
                num=(Decimal(request.data["num"])),
                material_name=material.name,
                material_item_name=material.item.name,
                material_unit=material.unit,
                date=formatted_date,
                is_send=False
            )
            werehouse[0].num += Decimal(request.data["num"])
            werehouse[0].save()
        else:
            gst = 0
            pst = 0
            drink_gst = 0
            bottle_deposit = 0
            recycle_fee = 0
            if material.is_gst : gst = round(Decimal(request.data["num"]) * material.value * Decimal(0.05),4)
            if material.is_pst : pst = round(Decimal(request.data["num"]) * material.value * Decimal(0.07),4)
            if material.is_drink_gst : drink_gst = round(Decimal(request.data["num"]) * material.value * Decimal(0.05),4)
            if material.is_bottle_deposit : bottle_deposit = material.bottle_num * 0.1
            if material.is_recycle_fee : recycle_fee = material.bottle_num * 0.02
            ShoppingHistory.objects.create(
                target_name = request.data["target_name"],
                value=round(Decimal(request.data["num"]) * material.value,4),
                gst= gst,
                pst= pst,
                bottle_deposit=bottle_deposit,
                recycle_fee=recycle_fee,
                drink_gst=drink_gst,
                num=(Decimal(request.data["num"])),
                material_name=material.name,
                material_item_name=material.item.name,
                material_parent_category_name=material.item.parent.name,
                material_unit=material.unit,
                material_position_name=",".join(material.role.values_list("name", flat=True)),
                date=formatted_date,
                is_send=False
            ) 
            werehouse[0].num -= Decimal(request.data["num"])
            werehouse[0].save()

        return Response(status=status.HTTP_200_OK)
    
class ShoppingHistoryReactJson(ModelViewSet):
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
        material = Material.objects.get(id=request.data["material_id"])
        werehouse = Warehouse.objects.get_or_create(material=material)

        datetime_object = datetime.strptime(request.data["date"], "%Y-%m-%d")
        formatted_date = datetime_object.strftime("%Y-%m-%d")

        if request.data["target_name"] == "warehouse" :
            WarehouseHistory.objects.create(
                target_name = request.data["target_name"],
                value=round(Decimal(request.data["num"]) * material.value,4),
                num=(Decimal(request.data["num"])),
                material_name=material.name,
                material_item_name=material.item.name,
                material_unit=material.unit,
                date=formatted_date,
                is_send=False
            )
            werehouse[0].num += Decimal(request.data["num"])
            werehouse[0].save()
        else:
            gst = 0
            pst = 0
            drink_gst = 0
            bottle_deposit = 0
            recycle_fee = 0
            if material.is_gst : gst = round(Decimal(request.data["num"]) * material.value * Decimal(0.05),4)
            if material.is_pst : pst = round(Decimal(request.data["num"]) * material.value * Decimal(0.07),4)
            if material.is_drink_gst : drink_gst = round(Decimal(request.data["num"]) * material.value * Decimal(0.05),4)
            if material.is_bottle_deposit : bottle_deposit = material.bottle_num * 0.1
            if material.is_recycle_fee : recycle_fee = material.bottle_num * 0.02
            ShoppingHistory.objects.create(
                target_name = request.data["target_name"],
                value=round(Decimal(request.data["num"]) * material.value,4),
                gst= gst,
                pst= pst,
                bottle_deposit=bottle_deposit,
                recycle_fee=recycle_fee,
                drink_gst=drink_gst,
                num=(Decimal(request.data["num"])),
                material_name=material.name,
                material_item_name=material.item.name,
                material_parent_category_name=material.item.parent.name,
                material_unit=material.unit,
                material_position_name=",".join(material.role.values_list("name", flat=True)),
                date=formatted_date,
                is_send=False
            ) 
            werehouse[0].num -= Decimal(request.data["num"])
            werehouse[0].save()

        return Response(status=status.HTTP_200_OK)