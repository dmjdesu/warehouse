from stock.models import *
from rest_framework import serializers
from datetime import datetime, timedelta
from pprint import pprint
from django.db.models import Sum

class ShoppingHistoryReactSerializer(serializers.ModelSerializer):
    total_num = serializers.SerializerMethodField()
    total_value = serializers.SerializerMethodField()

    class Meta:
        model = ShoppingHistory
        fields = ['total_num', 'total_value'] 
        datatables_always_serialize = ('id',)

    def get_total_num(self, obj):
        return obj.total_num

    def get_total_value(self, obj):
        return obj.total_value

class ShoppingHistorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ShoppingHistory
        fields = '__all__'

class MaterialSerializer(serializers.ModelSerializer):
    shopping_history_today = serializers.SerializerMethodField()
    shopping_history_yesterday = serializers.SerializerMethodField()

    class Meta:
        model = Material
        fields = '__all__' 

        datatables_always_serialize = ('id',)

    def get_shopping_history_today(self, obj):
        requested_date = self.context.get('requested_date') 
        queryset = ShoppingHistory.objects.filter(material_name=obj.name, date=requested_date)
        
        target_name = self.context.get('target_name') 
        if target_name != "all" and target_name != "undefined":
            queryset = queryset.filter(target_name=target_name)

        totals = queryset.aggregate(
            total_num=Sum('num'),
            total_value=Sum('value'),
        )

        return totals

    def get_shopping_history_yesterday(self, obj):
        requested_date = self.context.get('requested_date') 
        day_before_requested_date = requested_date - timedelta(days=1)  # Get the day before the requested date
        queryset = ShoppingHistory.objects.filter(material_name=obj.name, date=day_before_requested_date)
        target_name = self.context.get('target_name') 
        if target_name != "all" and target_name != "undefined":
            queryset = queryset.filter(target_name=target_name)

        totals = queryset.aggregate(
            total_num=Sum('num'),
            total_value=Sum('value'),
        )

        print(totals)
        
        return totals

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
