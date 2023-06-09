from decimal import Decimal
from django.contrib import admin

from .models import *
from .forms import WarehouseAdminForm
from django.db.models import Count, Sum #追加する
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from import_export import fields
from pprint import pprint
from rangefilter.filters import DateRangeFilter,NumericRangeFilter
from django_admin_listfilter_dropdown.filters import DropdownFilter
from more_admin_filters import MultiSelectDropdownFilter


class ShoppingHistoryProxyResource(resources.ModelResource):
    material_name = fields.Field()
    total_value = fields.Field()

    class Meta:
        fields = ['material_name','num','total_value', 'target_name','articles','date','is_send']
        model = ShoppingHistoryProxy

    def dehydrate_material_name(self, shopping_history):
        return '%s' % (shopping_history.material_name)

    def dehydrate_is_send(self, shopping_history):
        return "送信済み"  if shopping_history.is_send  else "未送信"

    def dehydrate_total_value(self, shopping_history):
        return '%s' % (shopping_history.num  * shopping_history.value)

class ShoppingHistoryResource(resources.ModelResource):
    class Meta:
        fields = ['target_name','material_name', "total"]
        model = ShoppingHistory
    
    def get_queryset():
            
        return super.get_queryset().values("total",'target_name','material_name','value','material_unit').annotate(total=Count('id')).order_by('-target_name')

class ShoppingHistoryProxyAdmin(ImportExportModelAdmin):
    ordering = ['-date']
    list_display = ('target_name','material_name','material_parent_category_name','num_unit','date','is_send','created_at')
    list_filter = [('target_name',MultiSelectDropdownFilter),'date',("material_position_name",MultiSelectDropdownFilter), ('material_item_name', MultiSelectDropdownFilter),'is_send',('material_name',MultiSelectDropdownFilter),('material_parent_category_name',MultiSelectDropdownFilter), ['date', DateRangeFilter],['value',NumericRangeFilter]]
    actions = ['send_material','no_send_material']
    list_per_page = 16384

    def num_unit(self,object):
        return str(object.num) + object.material_unit

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
    list_filter = [('target_name',MultiSelectDropdownFilter),("material_position_name",MultiSelectDropdownFilter),'date',('material_item_name',MultiSelectDropdownFilter),('material_name',MultiSelectDropdownFilter),('material_parent_category_name',MultiSelectDropdownFilter), ['date', DateRangeFilter]]
    list_display = ('material_parent_category_name','target_name','material_name','value','date','is_send')

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
            'total_value': Sum('value'),
            'total_gst': Sum('gst'),
            'total_pst': Sum('pst'),
            'total_bottle_deposit': Sum('bottle_deposit'),
            'total_recycle_fee': Sum('recycle_fee'),
            'total_drink_gst': Sum('drink_gst'),
            'total_tax_value': Sum('value') + Sum('drink_gst') + Sum('bottle_deposit') + Sum('recycle_fee') + Sum('gst') + Sum('pst'),
            'total_num': Sum('num'),
        }
        response.context_data['summary'] = list(
            qs
            .exclude(target_name="warehouse")
            .values('target_name','material_name','material_unit')
            .annotate(**metrics)
            .order_by('-target_name')
        )
        total_value = 0
        total_gst = 0
        total_pst = 0
        total_bottle_deposit = 0
        total_recycle_fee = 0
        total_drink_gst = 0
        total_tax_value = 0
        total_num = 0
        for data in  response.context_data['summary']:
            total_value += data["total_value"]
            total_gst += data["total_gst"]
            total_pst += data["total_pst"]
            total_bottle_deposit += data["total_bottle_deposit"]
            total_recycle_fee += data["total_recycle_fee"]
            total_drink_gst += data["total_drink_gst"]
            total_tax_value += data["total_tax_value"]
            total_num += data["total"]
        response.context_data['total_value'] = total_value
        response.context_data['total_gst'] = total_gst
        response.context_data['total_pst'] = total_pst
        response.context_data['total_bottle_deposit'] = total_bottle_deposit
        response.context_data['total_recycle_fee'] = total_recycle_fee
        response.context_data['total_drink_gst'] = total_drink_gst
        response.context_data['total_tax_value'] = total_tax_value
        response.context_data['total_num'] = total_num
        return response

    resource_class = ShoppingHistoryResource


class MaterialItemFilter(admin.SimpleListFilter):
    title = '中分類'
    parameter_name = 'material__item__parent'

    def lookups(self, request, model_admin):
        pprint("Warehouse")
        warehouse = Warehouse.objects.values_list("material__item__id","material__item__name",flat=False).filter(material__item__parent__id=request.GET.get("material__item__parent__id__exact")).distinct()
        return warehouse

    def queryset(self, request, queryset):
        pprint(self.value())
        if self.value():
            return queryset.filter(material__item__id=self.value())
        else:
            return queryset.all()

class ItemFilter(admin.SimpleListFilter):
    title = '中分類'
    parameter_name = 'item__parent'

    def lookups(self, request, model_admin):
        material = Material.objects.values_list("item__id","item__name",flat=False).filter(item__parent__id=request.GET.get("item__parent__id__exact")).distinct()
        return material

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(item__id=self.value())
        else:
            return queryset.all()

class MaterialAdmin(admin.ModelAdmin):
    list_display = ('name','place','unit','note')
    readonly_fields = ('value',)
    list_filter = ['item__parent',ItemFilter]
    list_per_page = 16384

class MaterialProxyAdmin(admin.ModelAdmin):
    list_display = ('name','unit','note')
    list_filter = ['item__parent',ItemFilter]

     

class InputFilter(admin.SimpleListFilter):
    template = 'admin/input_filter.html'

    def lookups(self, request, model_admin):
        # Dummy, required to show the filter.
        return ((),)

    def choices(self, changelist):
        # Grab only the "all" option.
        all_choice = next(super().choices(changelist))
        all_choice['query_parts'] = (
            (k, v)
            for k, v in changelist.get_filters_params().items()
            if k != self.parameter_name
        )
        yield all_choice

class ItemAdmin(admin.ModelAdmin):
    list_display = ('name','parent')
    list_filter = ['parent']

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user','affiliated_store')
    list_filter = ['affiliated_store']

class WarehouseAdmin(admin.ModelAdmin):
    list_display = ('material','num_unit')
    form = WarehouseAdminForm
    readonly_fields = ('num',)
    list_filter = ['material__item__parent',MaterialItemFilter]

    def num_unit(self,object):
        return str(object.num) + object.material.unit



admin.site.register(Item,ItemAdmin)
admin.site.register(Profile,ProfileAdmin)
admin.site.register(ShoppingHistory,ShoppingHistoryAdmin)
admin.site.register(ShoppingHistoryProxy,ShoppingHistoryProxyAdmin)
admin.site.register(Role)
admin.site.register(Material,MaterialAdmin)
admin.site.register(MaterialProxy,MaterialProxyAdmin)

admin.site.register(ParentCategory)
admin.site.register(Warehouse,WarehouseAdmin)