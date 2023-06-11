# Generated by Django 4.1.7 on 2023-04-24 05:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0024_material_role_alter_shoppinghistory_role'),
    ]

    operations = [
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('kitchen', 'Kitchen'), ('Sushi', 'Sushi'), ('dishup', 'Dish Up')], max_length=255)),
            ],
        ),
        migrations.RemoveField(
            model_name='material',
            name='role',
        ),
        migrations.RemoveField(
            model_name='shoppinghistory',
            name='role',
        ),
        migrations.AddField(
            model_name='material',
            name='role',
            field=models.ManyToManyField(to='stock.role'),
        ),
        migrations.AddField(
            model_name='shoppinghistory',
            name='role',
            field=models.ManyToManyField(to='stock.role'),
        ),
    ]
