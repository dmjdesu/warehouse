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

    class Meta:
        model = Material
        fields = '__all__' 

        datatables_always_serialize = ('id',)

    def get_shopping_history_today(self, obj):
        requested_date = self.context.get('requested_date') 
        queryset = ShoppingHistory.objects.filter(material_name=obj.name, date=requested_date)
        serializer = ShoppingHistorySerializer(queryset, many=True, context=self.context)
        return serializer.data

    def get_shopping_history_yesterday(self, obj):
        requested_date = self.context.get('requested_date') 
        day_before_requested_date = requested_date - timedelta(days=1)  # Get the day before the requested date
        queryset = ShoppingHistory.objects.filter(material_name=obj.name, date=day_before_requested_date)
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
