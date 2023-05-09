from django.shortcuts import render
from django.views.generic import CreateView
from django.shortcuts import redirect
from stock.forms import *
from stock.models import *
from django.contrib import messages
from django.shortcuts import resolve_url
from pprint import pprint
from django.contrib.messages.views import SuccessMessageMixin
from decimal import Decimal
from django.db.models.functions import Concat
from django.db.models import Value,F
from urllib.parse import urlencode
from django.core.cache import cache
from django.views import View

class ShoppingHistoryView(SuccessMessageMixin,CreateView):
    model = ShoppingHistory
    form_class = ShoppingHistoryForm
    template_name = "stock/form.html"
    success_message = "正常に登録されました。"

    def post(self, request, *args, **kwargs):
        material = Material.objects.get(id=request.POST["material"])        
        werehouse = Warehouse.objects.get_or_create(material=material)


        if request.POST["target_name"] == "warehouse" :
            
            try:
                WarehouseHistory.objects.create(
                    target_name = request.POST["target_name"],
                    value=round(Decimal(request.POST["num"]) * (material.value + material.extra),4),
                    num=(Decimal(request.POST["num"])),
                    material_name=material.name,
                    material_item_name=material.item.name,
                    material_unit=material.unit,
                    date=request.POST["date"],
                    is_send=False
                )
            except Exception:
                messages.error(self.request, '作成に失敗しました。原材料に商品が紐づかれているかなどの確認をお願いします。')
                return redirect("shopping_history")
            werehouse[0].num += Decimal(request.POST["num"])
        else:
            try:
                ShoppingHistory.objects.create(
                    target_name = request.POST["target_name"],
                    value=round(Decimal(request.POST["num"]) * (material.value + material.extra),4),
                    tax_value=round(Decimal(request.POST["num"]) * (material.value),4),
                    num=(Decimal(request.POST["num"])),
                    material_name=material.name,
                    material_item_name=material.item.name,
                    material_parent_category_name=material.item.parent.name,
                    material_unit=material.unit,
                    date=request.POST["date"],
                    is_send=False
                ) 
            except Exception:
                messages.error(self.request, '作成に失敗しました。原材料に商品が紐づかれているかなどの確認をお願いします。')
                return redirect("shopping_history")
            werehouse[0].num -= Decimal(request.POST["num"])
        
        
        
        werehouse[0].save()
        messages.success(self.request, '作成に成功しました。')

        base_url = '/admin/stock/shoppinghistory/add/'
        query_parameters = urlencode({'target_name': request.POST["target_name"]})
        url = '{}?{}'.format(base_url, query_parameters)
        return redirect(url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        parentcategory_list = cache.get('parentcategory_list')
        if parentcategory_list is None:
            parentcategory_list = ParentCategory.objects.annotate(item_material_role_name=F('item__material__role__name'))
            cache.set('parentcategory_list', parentcategory_list, 3600)
        context['parentcategory_list'] = parentcategory_list
        
        item_list = cache.get('item_list')
        if item_list is None:
            item_list = Item.objects.annotate(material_role_name=F('material__role__name'))
            cache.set('item_list', item_list, 3600)
        context['item_list'] = item_list

        material_list = cache.get('material_list')
        if material_list is None:
            material_list = Material.objects.annotate(role_name=F('role__name'))
            cache.set('material_list', material_list, 3600)
        context['material_list'] = material_list

        context['history_list'] = ShoppingHistory.objects.filter(is_send=False).order_by("-updated_at")
    
        return context

    def get_form_kwargs(self, *args, **kwargs):
        kwgs = super().get_form_kwargs(*args, **kwargs)
        material = cache.get('material')
        if material is None:
            material = list(Material.objects.annotate(full_name=Concat( Value('【') ,'place',Value('】'),'name')).values_list("id","full_name"))
            cache.set('material', material, 3600)
        kwgs["material"] = material
        try:
            kwgs["target_name"] = self.request.GET.get("target_name") if self.request.GET.get("target_name") else self.request.user.profile.affiliated_store
        except Exception:
            kwgs["target_name"] = self.request.GET.get("target_name")
        pprint(self.request.GET.get("target_name"))
        return kwgs
    
class RedirectToShoppingHistoryView(View):
    def get(self, request, *args, **kwargs):
        return redirect('shopping_history')

from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import render

from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import pandas as pd
import numpy as np
from datetime import date, datetime

class ShoppingPredictionView(View):
    def get(self, request, *args, **kwargs):
        df = self.prepare_dataframe()
        target_material_pairs = self.get_unique_pairs(df)
        today_ordinal = self.get_today_ordinal(df)

        predictions = {}
        model = LinearRegression()
        for pair in target_material_pairs:
            target_name, material_name = pair['target_name'], pair['material_name']
            target_df = self.filter_dataframe(df, target_name, material_name)
            X, y, X_date, y_date = self.create_train_test_data(target_df)
            model, model_date = self.fit_models(model, X, y, X_date, y_date)
            mse, rmse, y_pred = self.calculate_errors(model, X, y)
            next_date_pred, next_num = self.predict_next_date_and_num(model, model_date, target_df, today_ordinal)

            key = f"{target_name}_{material_name}"
            predictions[key] = {
                'mse': mse,
                'rmse': rmse,
                'predictions': y_pred.tolist() if y_pred is not None else None,
                'next_date': next_date_pred.isoformat(),
                'next_num': next_num,
            }

        return render(request, 'stock/predictions.html', {'predictions': predictions})

    def prepare_dataframe(self):
        shopping_data = ShoppingHistory.objects.values('date', 'target_name', 'material_name').annotate(total_num=Sum('num')).order_by('date')
        df = pd.DataFrame.from_records(shopping_data)
        df['date'] = pd.to_datetime(df['date'])
        df['date_ordinal'] = df['date'].apply(lambda x: x.toordinal())
        min_date_ordinal = df['date_ordinal'].min()
        df['date_ordinal'] -= min_date_ordinal
        return df

    def get_unique_pairs(self,df):
        return df[['target_name', 'material_name']].drop_duplicates().to_dict('records')

    def get_today_ordinal(self,df):
        today_date = datetime.now().date()
        return today_date.toordinal() - df['date_ordinal'].min()

    def filter_dataframe(self,df, target_name, material_name):
        return df[(df['target_name'] == target_name) & (df['material_name'] == material_name)]

    def create_train_test_data(self,target_df):
        X = target_df[['date_ordinal']]
        y = target_df['total_num']
        y_date = target_df['date_ordinal'].shift(-1).dropna()
        X_date = X.iloc[:-1, :]
        return X, y, X_date, y_date

    def fit_models(self,model, X, y, X_date, y_date):
        X_train, X_test, y_train, y_test = self.train_test_split_with_size_check(X, y)
        model.fit(X_train, y_train)

        if len(X_date) > 0:
            model_date = LinearRegression()
            X_train_date, X_test_date, y_train_date, y_test_date = self.train_test_split_with_size_check(X_date, y_date)
            model_date.fit(X_train_date, y_train_date)
        else:
            model_date = None

        return model, model_date

    def train_test_split_with_size_check(self,X, y, test_size=0.2, random_state=42):
        if len(X) > 5:
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)
        else:
            X_train, y_train = X, y
            X_test, y_test = None, None
        return X_train, X_test, y_train, y_test

    def calculate_errors(self,model, X, y):
        X_train, X_test, y_train, y_test = self.train_test_split_with_size_check(X, y)
        mse, rmse, y_pred = None, None, None
        if X_test is not None and y_test is not None:
            y_pred = model.predict(X_test)
            mse = mean_squared_error(y_test, y_pred)
            rmse = np.sqrt(mse)
        return mse, rmse, y_pred

    def predict_next_date_and_num(self, model, model_date, target_df, today_ordinal):
        min_date_ordinal = target_df['date_ordinal'].min()
        latest_date_ordinal = target_df['date_ordinal'].max()
        next_date_ordinal = max(latest_date_ordinal + 1, today_ordinal)
        X_next_date = np.array([[next_date_ordinal]])
        X_next = np.array([[next_date_ordinal]])

        if model_date is not None:
            next_date_ordinal_pred = round(model_date.predict(X_next_date)[0])
            next_date_ordinal_pred = min(next_date_ordinal_pred, today_ordinal + 365 * 100) # 100年以内に制限
            next_date_pred = date.fromordinal(next_date_ordinal_pred + min_date_ordinal)
        else:
            next_date_pred = date.fromordinal(today_ordinal + min_date_ordinal)

        next_num = round(model.predict(X_next)[0], 4)  # Round to 4 decimal places
        next_num = max(0, next_num)  # Ensure next_num is not negative
        return next_date_pred, next_num