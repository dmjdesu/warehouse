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
            material = Material.objects.get(
                name=history.material_name,
                item__name=history.material_item_name
            )
            history.material_position_name = ",".join(material.role.values_list("name", flat=True))
            history.save()