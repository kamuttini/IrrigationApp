# Generated by Django 2.2.10 on 2020-09-30 21:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0023_auto_20200930_1525'),
    ]

    operations = [
        migrations.AlterField(
            model_name='calendarirrigation',
            name='duration',
            field=models.CharField(choices=[('1 minuto ', '1 minuto '), ('2 minuti ', '2 minuti '), ('3 minuti ', '3 minuti '), ('4 minuti ', '4 minuti '), ('5 minuti ', '5 minuti '), ('6 minuti ', '6 minuti '), ('7 minuti ', '7 minuti '), ('8 minuti ', '8 minuti '), ('9 minuti ', '9 minuti '), ('10 minuti ', '10 minuti '), ('11 minuti ', '11 minuti '), ('12 minuti ', '12 minuti '), ('13 minuti ', '13 minuti '), ('14 minuti ', '14 minuti '), ('15 minuti ', '15 minuti '), ('20 minuti ', '20 minuti '), ('25 minuti ', '25 minuti '), ('30 minuti ', '30 minuti '), ('40 minuti ', '40 minuti '), ('30 minuti ', '30 minuti '), ('45 minuti ', '45 minuti '), ('50 minuti ', '50 minuti '), ('55 minuti ', '55 minuti '), ('60 minuti ', '60 minuti ')], default='20 minuti', max_length=100, verbose_name='durata'),
        ),
    ]
