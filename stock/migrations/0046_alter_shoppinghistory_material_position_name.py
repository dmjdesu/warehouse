# Generated by Django 4.1.7 on 2023-05-20 23:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0045_shoppinghistory_material_position_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shoppinghistory',
            name='material_position_name',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='材料のポジション'),
        ),
    ]
