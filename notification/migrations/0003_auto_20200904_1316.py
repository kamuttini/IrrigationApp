# Generated by Django 3.1 on 2020-09-04 11:16

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0002_notification_timestamp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2020, 9, 4, 11, 16, 55, 522176, tzinfo=utc)),
        ),
    ]
