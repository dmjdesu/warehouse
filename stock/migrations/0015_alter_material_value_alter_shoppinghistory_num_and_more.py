# Generated by Django 4.1.7 on 2023-03-18 05:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("stock", "0014_shoppinghistory_num_alter_shoppinghistory_value"),
    ]

    operations = [
        migrations.AlterField(
            model_name="material",
            name="value",
            field=models.DecimalField(
                blank=True,
                decimal_places=7,
                default=1,
                max_digits=12,
                null=True,
                verbose_name="価格",
            ),
        ),
        migrations.AlterField(
            model_name="shoppinghistory",
            name="num",
            field=models.DecimalField(
                blank=True,
                decimal_places=7,
                default=0,
                max_digits=12,
                null=True,
                verbose_name="数",
            ),
        ),
        migrations.AlterField(
            model_name="shoppinghistory",
            name="value",
            field=models.DecimalField(
                blank=True,
                decimal_places=7,
                default=0,
                max_digits=12,
                null=True,
                verbose_name="価格",
            ),
        ),
        migrations.AlterField(
            model_name="warehouse",
            name="num",
            field=models.DecimalField(
                blank=True,
                decimal_places=7,
                default=0,
                max_digits=12,
                null=True,
                verbose_name="数",
            ),
        ),
    ]
