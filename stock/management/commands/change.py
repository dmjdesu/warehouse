from django.core.management.base import BaseCommand
from stock.models import *
import time
from decimal import Decimal

class Command(BaseCommand):
    help = "テストコマンド"

    def handle(self, *args, **options):
        histories = ShoppingHistory.objects.all()
        for history in histories:
            material = Material.objects.get(
                name=history.material_name,
                item__name=history.material_item_name
            )
            gst = 0
            pst = 0
            drink_gst = 0
            bottle_deposit = 0
            recycle_fee = 0
            if material.is_gst : gst = round(history.num * material.value * Decimal(0.05),4)
            if material.is_pst : pst = round(history.num * material.value * Decimal(0.07),4)
            if material.is_drink_gst : drink_gst = round(history.num * material.value * Decimal(0.05),4)
            if material.is_bottle_deposit : bottle_deposit = round(material.bottle_num * Decimal(0.1),4)
            if material.is_recycle_fee : recycle_fee = round(material.bottle_num * Decimal(0.02),4)
            history.gst = gst
            history.pst = pst
            history.drink_gst = drink_gst
            history.bottle_deposit = bottle_deposit
            history.recycle_fee = recycle_fee
            history.save()