# Generated by Django 3.1 on 2020-08-27 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0005_auto_20200827_1930'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='data',
            field=models.DateTimeField(verbose_name='data'),
        ),
    ]
