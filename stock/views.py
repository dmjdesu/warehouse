from django.shortcuts import render
from django.views.generic import CreateView
from django.shortcuts import redirect
from stock.forms import ShoppingHistoryForm,PurchaseHistoryForm
from stock.models import *
from django.contrib import messages
from django.shortcuts import resolve_url
from pprint import pprint
from django.contrib.messages.views import SuccessMessageMixin
from decimal import Decimal

class ShoppingHistoryView(SuccessMessageMixin,CreateView):
    model = ShoppingHistory
    form_class = ShoppingHistoryForm
    template_name = "stock/form.html"
    success_message = "正常に登録されました。"

    def post(self, request, *args, **kwargs):
        pprint(request.POST)
        material = Material.objects.get(id=request.POST["material"])
        ShoppingHistory.objects.create(
            target_name = request.POST["target_name"],
            value=(Decimal(request.POST["num"]) / material.weight.num) * material.value,
            num=(Decimal(request.POST["num"])),
            material_name=material.name,
            material_unit=material.weight.unit,
            date=request.POST["date"]
        ) 
        pprint(material)
        werehouse = Warehouse.objects.get_or_create(material=material)
        werehouse[0].num -= Decimal(request.POST["num"])
        werehouse[0].save()
        messages.success(self.request, '作成に成功しました。')
        return redirect("/admin/")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['parentcategory_list'] = ParentCategory.objects.all()
        context['item_list'] = Item.objects.all()
        pprint(Item.objects.all())
        return context

    def get_form_kwargs(self, *args, **kwargs):
        kwgs = super().get_form_kwargs(*args, **kwargs)
        kwgs["material"] = list(Material.objects.values_list("id","name"))
        return kwgs
