# Generated by Django 4.2.2 on 2023-07-29 15:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='menu',
            options={'verbose_name': 'Menu'},
        ),
        migrations.AlterModelOptions(
            name='menuitem',
            options={'ordering': ['item_type', 'id'], 'verbose_name': 'Item'},
        ),
        migrations.AlterModelOptions(
            name='menuitempicture',
            options={'ordering': ['pk'], 'verbose_name': 'Item image'},
        ),
        migrations.AlterModelOptions(
            name='menuitemtype',
            options={'ordering': ['id'], 'verbose_name': 'MenuItemType', 'verbose_name_plural': 'Categories'},
        ),
        migrations.AlterModelOptions(
            name='order',
            options={'ordering': ['pk'], 'verbose_name': 'Order'},
        ),
        migrations.AlterModelOptions(
            name='orderitem',
            options={'ordering': ['pk'], 'verbose_name': 'Order item'},
        ),
        migrations.AlterModelOptions(
            name='restaurant',
            options={'ordering': ['pk'], 'verbose_name': 'Restaurant'},
        ),
        migrations.AlterModelOptions(
            name='table',
            options={'ordering': ['pk'], 'verbose_name': 'Table'},
        ),
        migrations.AddField(
            model_name='menuitemtype',
            name='restaurant',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='types', to='menu.restaurant'),
        ),
    ]
