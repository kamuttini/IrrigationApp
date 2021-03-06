# Generated by Django 3.1 on 2020-08-27 17:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0004_auto_20200827_1241'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('data', models.DateTimeField(verbose_name='data of the event')),
                ('type', models.CharField(max_length=200)),
            ],
        ),
        migrations.AlterField(
            model_name='area',
            name='last_irrigation',
            field=models.DateTimeField(default='2012-01-01 00:01', editable=False, verbose_name='date of irrigation'),
        ),
        migrations.AlterField(
            model_name='garden',
            name='last_rain',
            field=models.DateTimeField(default='2012-01-01 00:01', editable=False, verbose_name='date of last_rain'),
        ),
    ]
