from stock.models import *
from rest_framework import serializers
from datetime import datetime, timedelta

class ShoppingHistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = ShoppingHistory
        fields = '__all__' 

        datatables_always_serialize = ('id',)

class MaterialSerializer(serializers.ModelSerializer):
    shopping_history_today = serializers.SerializerMethodField()
    shopping_history_yesterday = serializers.SerializerMethodField()
    shopping_history_day_before_yesterday = serializers.SerializerMethodField()

    class Meta:
        model = Material
        fields = '__all__' 

        datatables_always_serialize = ('id',)

    def get_shopping_history_today(self, obj):
        today = datetime.now().date()
        queryset = ShoppingHistory.objects.filter(material_name=obj.name, date=today)
        serializer = ShoppingHistorySerializer(queryset, many=True, context=self.context)
        return serializer.data

    def get_shopping_history_yesterday(self, obj):
        yesterday = datetime.now().date() - timedelta(days=1)
        queryset = ShoppingHistory.objects.filter(material_name=obj.name, date=yesterday)
        serializer = ShoppingHistorySerializer(queryset, many=True, context=self.context)
        return serializer.data

    def get_shopping_history_day_before_yesterday(self, obj):
        day_before_yesterday = datetime.now().date() - timedelta(days=2)
        queryset = ShoppingHistory.objects.filter(material_name=obj.name, date=day_before_yesterday)
        serializer = ShoppingHistorySerializer(queryset, many=True, context=self.context)
        return serializer.data


class ItemSerializer(serializers.ModelSerializer):
    material_set = MaterialSerializer(many=True, read_only=True) 

    class Meta:
        model = Item
        fields = '__all__' 

class ParentCategorySerializer(serializers.ModelSerializer):
    item_set = ItemSerializer(many=True, read_only=True) 

    class Meta:
        model = ParentCategory
        fields = '__all__' 

        datatables_always_serialize = ('id',)
