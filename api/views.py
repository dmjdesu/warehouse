from django.db import transaction
from django.shortcuts import redirect
from django.views import View
from django.core.exceptions import ValidationError
from stock.models import *
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from pprint import pprint
from decimal import Decimal, InvalidOperation, ROUND_UP, ROUND_DOWN
from api.models import *
from api.serializers import *
from fractions import Fraction

class ParentCategoryJson(ModelViewSet):
    serializer_class = ParentCategorySerializer
    queryset = ParentCategory.objects.order_by("-name").prefetch_related('item_set')

    def get_queryset(self):
        queryset = ParentCategory.objects.order_by("-name").prefetch_related('item_set','item_set__material_set')
        category_name = self.request.GET.get('category_name') 
        if category_name != "all" and category_name != "undefined":
            queryset = queryset.filter(name=category_name)

        pprint("queryset")
        pprint(queryset.distinct().count())
        return queryset.distinct()
    
    def get_serializer_context(self):
        """
        Overriding the default method to add the 'requested_date' to the serializer context.
        """
        context = super().get_serializer_context()

        requested_date = self.request.GET.get('date')  # Get date from query parameter
        if requested_date:
            requested_date = datetime.strptime(requested_date, "%Y-%m-%d").date()  # Convert to datetime object
            context['requested_date'] = requested_date

        target_name = self.request.GET.get('target_name')  # Get date from query parameter
        if target_name:
            context['target_name'] = target_name

        category_name = self.request.GET.get('category_name')  # Get date from query parameter
        if category_name:
            context['category_name'] = category_name

        return context

class ShoppingHistoryJson(ModelViewSet):
    serializer_class = ShoppingHistorySerializer
    queryset = ShoppingHistory.objects.order_by("-updated_at")

    def get_queryset(self):
        queryset = None

        if self.kwargs.get('fk1'):
            queryset = ShoppingHistory.objects.order_by("-updated_at").filter(target_name=self.kwargs.get('fk1'))
        else:
            queryset = ShoppingHistory.objects.order_by("-updated_at")

        return queryset
    
    def create(self, request, *args, **kwargs):
        material = Material.objects.get(id=request.data["material_id"])
        werehouse = Warehouse.objects.get_or_create(material=material)

        datetime_object = datetime.strptime(request.data["date"], "%Y-%m-%d")
        formatted_date = datetime_object.strftime("%Y-%m-%d")

        print("create")

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
            # 小数点以下4桁に丸めるための値を定義
            four_places = Decimal('0.0001')

            # 以下のように、各税金や料金を計算する際にquantizeメソッドを使用して小数点以下4桁に丸めます。
            if material.is_gst:
                gst = (Decimal(request.data["num"]) * Decimal(material.value) * Decimal(0.05)).quantize(four_places, ROUND_DOWN)
            if material.is_pst:
                pst = (Decimal(request.data["num"]) * Decimal(material.value) * Decimal(0.07)).quantize(four_places, ROUND_DOWN)
            if material.is_drink_gst:
                drink_gst = (Decimal(request.data["num"]) * Decimal(material.value) * Decimal(0.05)).quantize(four_places, ROUND_DOWN)
            if material.is_bottle_deposit:
                bottle_deposit = (Decimal(material.bottle_num) * Decimal(0.1)).quantize(four_places, ROUND_DOWN)
            if material.is_recycle_fee:
                recycle_fee = (Decimal(material.bottle_num) * Decimal(0.02)).quantize(four_places, ROUND_DOWN)

            # 計算された値を四捨五入してShoppingHistoryオブジェクトを作成します。
            value = (Decimal(request.data["num"]) * Decimal(material.value)).quantize(four_places, ROUND_DOWN)

            ShoppingHistory.objects.create(
                target_name = request.data["target_name"],
                value=value,
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
            # 小数点以下4桁で切り上げるためのコンテキストを作成
            four_places = Decimal('0.0001')
            # もしGSTが適用されるなら
            if material.is_gst:
                gst = (Decimal(request.data["num"]) * Decimal(material.value) * Decimal(0.05)).quantize(four_places, rounding=ROUND_UP)

            # もしPSTが適用されるなら
            if material.is_pst:
                pst = (Decimal(request.data["num"]) * Decimal(material.value) * Decimal(0.07)).quantize(four_places, rounding=ROUND_UP)

            # もし飲料にGSTが適用されるなら
            if material.is_drink_gst:
                drink_gst = (Decimal(request.data["num"]) * Decimal(material.value) * Decimal(0.05)).quantize(four_places, rounding=ROUND_UP)

            # もしボトルデポジットが適用されるなら
            if material.is_bottle_deposit:
                bottle_deposit = (Decimal(material.bottle_num) * Decimal(0.1)).quantize(four_places, rounding=ROUND_UP)

            # もしリサイクル料金が適用されるなら
            if material.is_recycle_fee:
                recycle_fee = (Decimal(material.bottle_num) * Decimal(0.02)).quantize(four_places, rounding=ROUND_UP)
            print(gst)
            print(pst)
            try:
                # データベーストランザクションの開始
                with transaction.atomic():
                    # 各フィールドを個別に処理
                 
                    # 小数点以下4桁に丸めるための値を定義
                    four_places = Decimal('0.0001')
                    value = (Decimal(request.data["num"]) * Decimal(material.value)).quantize(four_places, ROUND_DOWN)
                    num = Decimal(request.data["num"])
                    print("value2")
                    print(value)
                    
                    # オブジェクトの作成
                    shopping_history = ShoppingHistory(
                        target_name=request.data["target_name"],
                        value=value,
                        gst=gst,
                        pst=pst,
                        bottle_deposit=bottle_deposit,
                        recycle_fee=recycle_fee,
                        drink_gst=drink_gst,
                        num=num,
                        material_name=material.name,
                        material_item_name=material.item.name,
                        material_parent_category_name=material.item.parent.name,
                        material_unit=material.unit,
                        material_position_name=",".join(material.role.values_list("name", flat=True)),
                        date=formatted_date,
                        is_send=False
                    )

                    # 保存前の検証を行う
                    shopping_history.full_clean()

                    # データベースに保存
                    shopping_history.save()
            except InvalidOperation as e:
                # ここでどの項目でエラーが起きたかを判断する
                error_field = "value" if 'value' in str(e) else "num"  # この例では 'value' と 'num' のみチェックしています
                error_message = f"Invalid input for {error_field}: {e}"
                print(error_message)
                # 適切なエラーレスポンスを返す
            except Exception as e:
                # その他のエラー
                print(f"An unexpected error occurred: {e}")
                # 適切なエラーレスポンスを返す
            werehouse[0].num -= Decimal(request.data["num"])
            werehouse[0].save()

        return Response(status=status.HTTP_200_OK)