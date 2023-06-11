# Generated by Django 4.1.7 on 2023-05-09 07:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0040_material_extra'),
    ]

    operations = [
        migrations.AddField(
            model_name='shoppinghistory',
            name='tax_value',
            field=models.DecimalField(blank=True, decimal_places=4, default=0, max_digits=12, null=True, verbose_name='税込価格'),
        ),
    ]
