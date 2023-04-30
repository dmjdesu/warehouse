from django import forms
from stock.models import *
import datetime
from bootstrap_datepicker_plus.widgets import DatePickerInput

class ShopChoices(models.TextChoices):
    ALL = "",""
    KITCHEN = 'kitchen', 'Kitchen'
    HOLE = 'Sushi', 'Sushi'
    OTHER = 'dishup', 'Dish Up'

class ShoppingHistoryForm(forms.ModelForm):
    target_name = forms.fields.ChoiceField(
        choices=TargetChoices.choices,
        required=True,
        label='店舗',
        # widget=forms.widgets.Select,
    )
    role = forms.ModelChoiceField(
        label='店舗カテゴリー',
        queryset=Role.objects,
        required=False
    )
    
    date = forms.DateTimeField(widget=DatePickerInput(format='%Y-%m-%d'))
    parent_category = forms.ModelChoiceField(
        label='親カテゴリ',
        queryset=ParentCategory.objects,
        required=False
    )
    item = forms.ModelChoiceField(
        label='子カテゴリ',
        queryset=Item.objects,
        required=False
    )
    material = forms.ModelChoiceField(
        label='原材料',
        queryset=Material.objects,
        required=True
    )
    num = forms.IntegerField(label="量", widget=forms.NumberInput(attrs={'step': 0.01}))
    field_order = ('target_name','parent_category', 'item',"material","role")
    class Meta:
        model = ShoppingHistory
        fields = ("date","value")
    def __init__(self, material=None,target_name=None,*args, **kwargs):
        self.base_fields["material"].choices = material
        self.base_fields["target_name"].initial = target_name
        super().__init__(*args, **kwargs)

class PurchaseHistoryForm(forms.ModelForm):
    item = forms.ChoiceField()
    date = forms.DateTimeField(widget=DatePickerInput(format='%Y-%m-%d'))
    class Meta:
        model = PurchaseHistory
        fields = "__all__"
    def __init__(self, item=None,*args, **kwargs):
        self.base_fields["item"].choices = item
        super().__init__(*args, **kwargs)

class CustomChoiceField(forms.ModelChoiceField):
    #ここで表示したい形式にします
    def label_from_instance(self, obj):
        return u'%s %s' %(obj.name,obj.unit) if(obj.unit) else ""
        

class WarehouseAdminForm(forms.ModelForm):
    """Django 管理サイト専用のフォーム
    """
    material = CustomChoiceField(queryset=Material.objects.all())
    class Meta:
        model = Warehouse
        fields = [
                'num',
                ]
 

 