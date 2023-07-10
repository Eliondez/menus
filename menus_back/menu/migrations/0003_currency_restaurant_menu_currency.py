# Generated by Django 4.2.2 on 2023-07-10 16:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0002_alter_menuitem_options_menuitemtype_description_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('char_code', models.CharField(max_length=8, primary_key=True, serialize=False)),
                ('sign', models.CharField(blank=True, max_length=1)),
                ('from_left', models.BooleanField(blank=True, default=True)),
                ('separated', models.BooleanField(blank=True, default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('enabled', models.BooleanField(blank=True, default=True)),
            ],
        ),
        migrations.AddField(
            model_name='menu',
            name='currency',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, to='menu.currency'),
        ),
    ]
