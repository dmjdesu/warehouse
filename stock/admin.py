from django.contrib import admin

from .models import *
from .forms import WarehouseAdminForm
from django.db.models import Count, Sum #追加する
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from import_export import fields
from pprint import pprint
from rangefilter.filters import DateRangeFilter,NumericRangeFilter

class ShoppingHistoryProxyResource(resources.ModelResource):
    material_name = fields.Field()
    total_value = fields.Field()

    class Meta:
        fields = ['material_name','num','total_value', 'target_name','articles','date','is_send']
        model = ShoppingHistoryProxy

    def dehydrate_material_name(self, shopping_history):
        return '%s' % (shopping_history.material)

    def dehydrate_is_send(self, shopping_history):
        return "送信済み"  if shopping_history.is_send  else "未送信"

    def dehydrate_total_value(self, shopping_history):
        return '%s' % (shopping_history.num  * shopping_history.material.value)

class ShoppingHistoryResource(resources.ModelResource):
    class Meta:
        fields = ['target_name','material__name', "total"]
        model = ShoppingHistory
    
    def get_queryset():

        metrics = {
            'total': Count('id'),
            'total_num': Sum('num'),
        }
            
        return super.get_queryset().values("total",'target_name','material__name','material__value','material__unit').annotate(total=Count('id')).order_by('-target_name')

class ShoppingHistoryProxyAdmin(ImportExportModelAdmin):
    # ImportExportModelAdminを利用するようにする
    ordering = ['-date']
    list_display = ('target_name','material','articles','date','is_send')
    list_filter = ['target_name','date','is_send','material', ['date', DateRangeFilter],['num',NumericRangeFilter]]
    actions = ['send_material','no_send_material']

    def articles(self,object):
        pprint(object.material.weight.unit)
        return str(object.num * object.material.weight.num) + object.material.weight.unit

    @admin.action(
        description="全て発送済みにする",
        permissions=("change",),
    )
    def send_material(self,request,queryset):
        queryset.update(is_send=True)
    
    @admin.action(
        description="全て未発送にする",
        permissions=("change",),
    )
    def no_send_material(self,request,queryset):
        queryset.update(is_send=False)

class ShoppingHistoryAdmin(admin.ModelAdmin):
    change_list_template = 'admin/history_change_list.html'
    date_hierarchy = 'date'
    list_filter = ['target_name','date','material', ['date', DateRangeFilter]]
    list_display = ('target_name','material','num','date','is_send')

    def regroup_by(self):
        return 'date'
    
    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(
            request,
            extra_context=extra_context,
        )
        try:
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            return response
        metrics = {
            'total': Count('id'),
            'total_num': Sum('num'),
        }
        response.context_data['summary'] = list(
            qs
            .values('target_name','material__name','material__value','material__weight__unit','material__weight__num')
            .annotate(**metrics)
            .order_by('-target_name')
        )
        total_value = 0
        for data in  response.context_data['summary']:
            total_value += int(data["total_num"] / data["material__weight__num"]) * data["material__value"]
        response.context_data['total_value'] = total_value
        return response

    # resource_class = ShoppingHistoryResource


class ItemAdmin(admin.ModelAdmin):
    list_display = ('name','value')

class MaterialAdmin(admin.ModelAdmin):
    list_display = ('name','weight')

class WarehouseAdmin(admin.ModelAdmin):
    list_display = ('material','num')
    form = WarehouseAdminForm
    list_filter = ['material',]

class WeightAdmin(admin.ModelAdmin):
    list_display = ('num','unit')

admin.site.register(Item)
admin.site.register(Weight,WeightAdmin)
admin.site.register(ShoppingHistory,ShoppingHistoryAdmin)
admin.site.register(ShoppingHistoryProxy,ShoppingHistoryProxyAdmin)
admin.site.register(Material,MaterialAdmin)
admin.site.register(ParentCategory)
admin.site.register(Warehouse,WarehouseAdmin)