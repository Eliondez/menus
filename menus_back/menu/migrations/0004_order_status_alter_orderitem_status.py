# Generated by Django 4.2.2 on 2023-08-02 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0003_alter_menuitemtype_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.PositiveSmallIntegerField(choices=[(0, 'in_work'), (1, 'completed')], default=0),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='status',
            field=models.CharField(choices=[('ordered', 'ordered'), ('preparing', 'preparing')], default='ordered', max_length=128),
        ),
    ]
