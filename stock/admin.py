from django.contrib import admin

from .models import Material,ShoppingHistory,Category,ParentCategory,Warehouse,ShoppingHistoryProxy
from django.db.models import Count, Sum #追加する
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from import_export import fields
from pprint import pprint

class ShoppingHistoryResource(resources.ModelResource):
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

class ShoppingHistoryProxyAdmin(ImportExportModelAdmin):
    # ImportExportModelAdminを利用するようにする
    ordering = ['-date']
    list_display = ('target_name','material','articles','date','is_send')
    list_filter = ['target_name','date','is_send']
    actions = ['send_material','no_send_material']

    def articles(self,object):
        return str(object.num) + object.material.unit

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

    # django-import-exportsの設定
    resource_class = ShoppingHistoryResource

class ShoppingHistoryAdmin(ImportExportModelAdmin):
    change_list_template = 'admin/history_change_list.html'
    date_hierarchy = 'date'
    list_filter = ['target_name','date']
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
            .values('target_name','material__name','material__value','material__unit')
            .annotate(**metrics)
            .order_by('-target_name')
        )
        total_value = 0
        for data in  response.context_data['summary']:
            total_value += data["total_num"] * data["material__value"]
        response.context_data['total_value'] = total_value
        return response

    resource_class = ShoppingHistoryResource


class ItemAdmin(admin.ModelAdmin):
    list_display = ('name','value')

class MaterialAdmin(admin.ModelAdmin):
    list_display = ('name', 'unit')

class ItemMaterialAdmin(admin.ModelAdmin):
    list_display = ('item', 'material','num')

class WarehouseAdmin(admin.ModelAdmin):
    list_display = ('material','num')
    list_filter = ['material','material__category','material__category__parent']

admin.site.register(Category)
admin.site.register(ShoppingHistory,ShoppingHistoryAdmin)
admin.site.register(ShoppingHistoryProxy,ShoppingHistoryProxyAdmin)
admin.site.register(Material,MaterialAdmin)
admin.site.register(ParentCategory)
admin.site.register(Warehouse,WarehouseAdmin)