# Generated by Django 4.2.2 on 2023-08-05 16:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0005_remove_order_menu_alter_table_num'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='pay_type',
            field=models.PositiveSmallIntegerField(blank=True, choices=[(0, 'cash'), (1, 'card')], null=True),
        ),
    ]
