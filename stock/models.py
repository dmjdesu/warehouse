from __future__ import barry_as_FLUFL
from django.db import models
from datetime import date
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class TargetChoices(models.TextChoices):
    PENTICNTON = 'penticton', 'ペンティクトン店'
    WEST = 'west', 'ウエスト'
    KOYA = 'koya', 'KOYA'
    WAREHOUSE = 'warehouse', '倉庫'
    MEAT = 'others', 'OTHERS'
    CENTRAL = 'central', 'セントラルキッチン'

class ShopChoices(models.TextChoices):
    KITCHEN = 'kitchen', 'Kitchen'
    HOLE = 'Sushi', 'Sushi'
    OTHER = 'dishup', 'Dish Up'


class UnitChoices(models.TextChoices):
    GRAM = 'g', 'グラム'
    PACK = 'p', 'パック'
    LB = 'lb', 'LB'
    CASE = 'cs', 'ケース'
    BOX = "box", "ボックス"
    SET = "set", "セット"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    affiliated_store =  models.CharField(max_length=255,choices=TargetChoices.choices)

class Role(models.Model):
    name = models.CharField(max_length=255,choices=ShopChoices.choices)

    def __str__(self):
        return self.name


class ParentCategory(models.Model):
    name = models.CharField('親カテゴリ名', max_length=255)

    def __str__(self):
        return self.name


class Item(models.Model):
    name = models.CharField('カテゴリ名', max_length=255)
    parent = models.ForeignKey(ParentCategory, verbose_name='親カテゴリ', on_delete=models.PROTECT)

    def __str__(self):
        return self.name


class Material(models.Model):
    name = models.CharField(verbose_name='材料名',max_length=255)
    place = models.CharField(verbose_name='場所名',max_length=255)
    role = models.ManyToManyField(Role, blank=True)
    item = models.ForeignKey(Item, verbose_name='カテゴリ', on_delete=models.PROTECT,blank=True,null=True,)
    value = models.DecimalField(verbose_name='価格',max_digits=12,decimal_places=4,blank=True,null=True,default=1)
    extra = models.DecimalField(verbose_name='税金及び余分にかかる費用',max_digits=12,decimal_places=4,blank=True,null=True,default=0)
    unit = models.CharField(verbose_name='単位',max_length=255,choices=UnitChoices.choices)
    note = models.TextField(null=True,blank=True)
    def __str__(self):
        return self.name

class MaterialProxy(Material):
    class Meta:
        proxy = True

def get_deleted_material():
    return Material.objects.get_or_create(name="削除された材料")[0]

def get_deleted_item():
    return Item.objects.get_or_create(name="削除された商品")[0]




#倉庫から店舗に仕入れがどれほどあったか
#これらの統計をとる
class ShoppingHistory(models.Model):
    target_name = models.CharField(max_length=255,choices=TargetChoices.choices)
    value = models.DecimalField(verbose_name='価格',max_digits=12,decimal_places=4,blank=True,null=True,default=0)
    tax_value = models.DecimalField(verbose_name='税込価格',max_digits=12,decimal_places=4,blank=True,null=True,default=0)
    num = models.DecimalField(verbose_name='数',max_digits=12,decimal_places=4,blank=True,null=True,default=0)
    material_name = models.CharField(verbose_name='材料名',max_length=255)
    material_item_name = models.CharField(verbose_name='材料の商品名',max_length=255)
    material_parent_category_name = models.CharField(verbose_name='材料の親カテゴリー名',max_length=255)
    material_unit = models.CharField(verbose_name='単位',max_length=255)
    date = models.DateField(help_text='注文日',default=date.today) 
    is_send = models.BooleanField(null=True, blank=True,default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

#倉庫にどれほどの仕入れがあったか
class WarehouseHistory(models.Model):
    target_name = models.CharField(max_length=255,choices=TargetChoices.choices)
    value = models.DecimalField(verbose_name='価格',max_digits=12,decimal_places=4,blank=True,null=True,default=0)
    num = models.DecimalField(verbose_name='数',max_digits=12,decimal_places=4,blank=True,null=True,default=0)
    material_name = models.CharField(verbose_name='材料名',max_length=255)
    material_item_name = models.CharField(verbose_name='材料の商品名',max_length=255)
    material_unit = models.CharField(verbose_name='単位',max_length=255)
    date = models.DateField(help_text='作成日',default=date.today) 
    is_send = models.BooleanField(null=True, blank=True,default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class ShoppingHistoryProxy(ShoppingHistory):
    class Meta:
        proxy = True


#倉庫の数
class Warehouse(models.Model):
    material = models.ForeignKey(Material, verbose_name='原材料', on_delete=models.SET(get_deleted_material))
    num = models.DecimalField(verbose_name='数',max_digits=12,decimal_places=4,blank=True,null=True,default=0)

#どれほど販売がされたか
#これらの統計をとる
class PurchaseHistory(models.Model):
    target_name = models.CharField(max_length=255,choices=TargetChoices.choices)
    item = models.ForeignKey(Item, verbose_name='アイテム', on_delete=models.SET(get_deleted_item))
    num = models.IntegerField(verbose_name='数',default=0)
    date = models.DateField(help_text='作成日')
