from django import forms
from stock.models import *
from django.utils import timezone
from bootstrap_datepicker_plus.widgets import DatePickerInput
TARGET = (
    ('penticton', 'ペンティクトン店'),
    ('west', 'ウエスト'),
    ('koya', 'KOYA'),
    ('others', 'OTHERS'),
    ('central', 'セントラルキッチン'),
)

class ShoppingHistoryForm(forms.ModelForm):
    target_name = forms.fields.ChoiceField(
        choices=TargetChoices.choices,
        required=True,
        label='店舗',
        # widget=forms.widgets.Select,
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
        required=False
    )
    field_order = ('target_name','parent_category', 'item',"material")
    class Meta:
        model = ShoppingHistory
        fields = ("date","num")
    def __init__(self, material=None,*args, **kwargs):
        self.base_fields["material"].choices = material
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
