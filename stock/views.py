from django.shortcuts import render
from django.views.generic import CreateView
from django.shortcuts import redirect
from stock.forms import ShoppingHistoryForm,PurchaseHistoryForm
from stock.models import ParentCategory, ShoppingHistory,PurchaseHistory,Item,Material,Warehouse
from django.contrib import messages
from django.shortcuts import resolve_url
from pprint import pprint

class ShoppingHistoryView(CreateView):
    model = ShoppingHistory
    form_class = ShoppingHistoryForm
    template_name = "stock/form.html"

    def post(self, request, *args, **kwargs):
        material = Material.objects.get(id=request.POST["material"])
        pprint(request.POST)
        ShoppingHistory.objects.create(
            target_name = request.POST["target_name"],
            num=request.POST["num"],
            material=material,
            date=request.POST["date"]
        ) 
        werehouse = Warehouse.objects.get_or_create(material=material)
        werehouse[0].num -= int(request.POST["num"])
        werehouse[0].save()
        pprint(werehouse[0].num)
        return redirect("/admin/")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['parentcategory_list'] = ParentCategory.objects.all()
        context['category_list'] = Item.objects.all()
        return context

    # 投稿に成功した時に実行される処理
    def get_success_url(self):
        messages.success(self.request, '記事を投稿しました。')
        return resolve_url('stock')

    def get_form_kwargs(self, *args, **kwargs):
        kwgs = super().get_form_kwargs(*args, **kwargs)
        kwgs["material"] = list(Material.objects.values_list("id","name"))
        return kwgs
