from django.core.management.base import BaseCommand
from stock.models import *
import time
from decimal import Decimal
import pprint

class Command(BaseCommand):
    help = "テストコマンド"

    def handle(self, *args, **options):
        histories = ShoppingHistory.objects.all()
        for history in histories:
            try:
                material = Material.objects.get(
                    name=history.material_name,
                    item__name=history.material_item_name
                )
            except:
                print(history.material_name)
                if(history.material_name == "Sriracha sauce"):
                    history.material_name = "Siracha sauce"

                if(history.material_name == "Sesami dressing(代用）"):
                    history.material_name = "Sesami dressing"

                if(history.material_name == "cha-shu"):
                    history.material_name = "Cha-shu"
            gst = 0
            pst = 0
            drink_gst = 0
            bottle_deposit = 0
            recycle_fee = 0
            if material.is_gst : gst = Decimal(history.num) * Decimal(material.value) * Decimal(0.05)
            if material.is_pst : pst = Decimal(history.num) * Decimal(material.value) * Decimal(0.07)
            if material.is_drink_gst : drink_gst = Decimal(history.num) * Decimal(material.value) * Decimal(0.05)
            if material.is_bottle_deposit : bottle_deposit = Decimal(material.bottle_num) * Decimal(0.1)
            if material.is_recycle_fee : recycle_fee = Decimal(material.bottle_num) * Decimal(0.02)

            history.gst = gst
            history.pst = pst
            history.drink_gst = drink_gst
            history.bottle_deposit = bottle_deposit
            history.recycle_fee = recycle_fee
            history.value = Decimal(history.num) * Decimal(material.value)
            history.save()