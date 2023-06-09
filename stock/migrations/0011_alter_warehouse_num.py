# Generated by Django 4.1.7 on 2023-03-18 04:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("stock", "0010_alter_shoppinghistory_material_unit"),
    ]

    operations = [
        migrations.AlterField(
            model_name="warehouse",
            name="num",
            field=models.DecimalField(
                blank=True,
                decimal_places=10,
                default=0,
                max_digits=12,
                null=True,
                verbose_name="数",
            ),
        ),
    ]
