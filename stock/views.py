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
        material = Material.objects.get(id=request.POST["material"])        
        werehouse = Warehouse.objects.get_or_create(material=material)
        
        if request.POST["target_name"] == "warehouse" :
            WarehouseHistory.objects.create(
                target_name = request.POST["target_name"],
                value=round(Decimal(request.POST["num"]) * material.value,4),
                num=(Decimal(request.POST["num"])),
                material_name=material.name,
                material_item_name=material.item.name,
                material_unit=material.unit,
                date=request.POST["date"],
                is_send=False
            )
            werehouse[0].num += Decimal(request.POST["num"])
        else:
            ShoppingHistory.objects.create(
                target_name = request.POST["target_name"],
                value=round(Decimal(request.POST["num"]) * material.value,4),
                num=(Decimal(request.POST["num"])),
                material_name=material.name,
                material_item_name=material.item.name,
                material_unit=material.unit,
                date=request.POST["date"],
                is_send=False
            ) 
            werehouse[0].num -= Decimal(request.POST["num"])
        
        
        werehouse[0].save()
        messages.success(self.request, '作成に成功しました。')
        return redirect("shopping_history")

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

from django.http import JsonResponse
from django.views import View
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import pandas as pd
import numpy as np
from datetime import date
from .models import ShoppingHistory

class ShoppingPredictionView(View):
    template_name = "stock/predicitions.html"
    def get(self, request, *args, **kwargs):
        shopping_data = ShoppingHistory.objects.all().values()
        df = pd.DataFrame.from_records(shopping_data)
        df['date'] = pd.to_datetime(df['date'])
        df['date_ordinal'] = df['date'].apply(lambda x: x.toordinal())
        target_material_pairs = df[['target_name', 'material_name']].drop_duplicates().to_dict('records')
        

        predictions = {}
        for pair in target_material_pairs:
            target_name = pair['target_name']
            material_name = pair['material_name']
            target_df = df[(df['target_name'] == target_name) & (df['material_name'] == material_name)]
            X = target_df[['date_ordinal', 'value']]
            y = target_df['num']

            if len(X) > 5:
                # Enough data, perform train-test split
                X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            else:
                # Not enough data, use all data as training set
                X_train, y_train = X, y
                X_test, y_test = None, None

            model = LinearRegression()
            model.fit(X_train, y_train)

            mse, rmse, y_pred = None, None, None
            if X_test is not None and y_test is not None:
                y_pred = model.predict(X_test)
                mse = mean_squared_error(y_test, y_pred)
                rmse = np.sqrt(mse)

            latest_date_ordinal = target_df['date_ordinal'].max()
            next_date_ordinal = latest_date_ordinal + 1
            X_next = np.array([[next_date_ordinal, 0]])
            next_num = round(model.predict(X_next)[0], 4) 
            next_date = date.fromordinal(next_date_ordinal)

            key = f"{target_name}_{material_name}"
            predictions[key] = {
                'mse': mse,
                'rmse': rmse,
                'predictions': y_pred.tolist() if y_pred is not None else None,
                'next_date': next_date.isoformat(),
                'next_num': next_num,
            }

        return render(request, 'stock/predictions.html', {'predictions': predictions})