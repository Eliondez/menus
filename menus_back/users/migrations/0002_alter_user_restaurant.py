# Generated by Django 4.2.2 on 2023-07-29 15:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0002_alter_menu_options_alter_menuitem_options_and_more'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='restaurant',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='users', to='menu.restaurant'),
        ),
    ]
