# Generated by Django 2.2.10 on 2020-11-23 22:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0033_merge_20201123_2321'),
    ]

    operations = [
        migrations.AlterField(
            model_name='garden',
            name='last_rain',
            field=models.DateTimeField(verbose_name='ultima pioggia'),
        ),
    ]
