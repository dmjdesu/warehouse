# Generated by Django 4.1.7 on 2023-04-30 01:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0028_remove_shoppinghistory_role'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shoppinghistory',
            name='material_role_name',
        ),
    ]