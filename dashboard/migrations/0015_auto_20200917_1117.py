# Generated by Django 2.2.10 on 2020-09-17 09:17

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0014_delete_event'),
    ]

    operations = [
        migrations.AlterField(
            model_name='garden',
            name='next_rain',
            field=models.DateTimeField(default=datetime.date(2020, 9, 17)),
        ),
        migrations.CreateModel(
            name='Irrigation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('irrigation', models.DateTimeField(verbose_name='date of irrigation')),
                ('duration', models.TimeField()),
                ('irrigation_type', models.CharField(choices=[('M', 'Manuale'), ('C', 'Calendario'), ('S', 'Intelligente')], default='M', max_length=1)),
                ('area', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='dashboard.Area')),
            ],
        ),
    ]
