from django.core.management.base import BaseCommand
from stock.models import *
import time

class Command(BaseCommand):
    help = "テストコマンド"

    def handle(self, *args, **options):
        histories = ShoppingHistory.objects.all()
        for history in histories:
            material = Material.objects.get(
                name=history.material_name,
                item__name=history.material_item_name
            )
            if material.extra != 0:
                history.tax_value = history.value + (material.extra * history.num)
            else:
                history.tax_value = history.value
            history.save()