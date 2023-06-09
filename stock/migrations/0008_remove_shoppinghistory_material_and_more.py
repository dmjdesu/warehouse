# Generated by Django 4.1.7 on 2023-03-18 03:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("stock", "0007_material_item_material_value_material_weight"),
    ]

    operations = [
        migrations.RemoveField(model_name="shoppinghistory", name="material",),
        migrations.RemoveField(model_name="shoppinghistory", name="num",),
        migrations.AddField(
            model_name="shoppinghistory",
            name="material_name",
            field=models.CharField(default="", max_length=255, verbose_name="材料名"),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="shoppinghistory",
            name="value",
            field=models.DecimalField(
                blank=True,
                decimal_places=10,
                default=1,
                max_digits=12,
                null=True,
                verbose_name="価格",
            ),
        ),
    ]
