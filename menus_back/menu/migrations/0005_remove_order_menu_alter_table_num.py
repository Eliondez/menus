# Generated by Django 4.2.2 on 2023-08-02 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0004_order_status_alter_orderitem_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='menu',
        ),
        migrations.AlterField(
            model_name='table',
            name='num',
            field=models.CharField(max_length=128, unique=True),
        ),
    ]