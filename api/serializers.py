from stock.models import *
from rest_framework import serializers

class ShoppingHistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = ShoppingHistory
        fields = "__all__"