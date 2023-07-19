# Generated by Django 4.2.2 on 2023-07-15 16:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0006_restaurant_address_restaurant_currency'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='menu',
            name='currency',
        ),
        migrations.AddField(
            model_name='restaurant',
            name='menu',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='active_restaurants', to='menu.menu'),
        ),
        migrations.AlterField(
            model_name='menu',
            name='restaurant',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='menus', to='menu.restaurant'),
        ),
    ]
