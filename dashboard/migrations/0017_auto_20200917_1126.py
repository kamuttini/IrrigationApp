# Generated by Django 2.2.10 on 2020-09-17 09:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0016_auto_20200917_1123'),
    ]

    operations = [
        migrations.AlterField(
            model_name='irrigation',
            name='irrigation',
            field=models.DateField(verbose_name='date of irrigation'),
        ),
    ]
