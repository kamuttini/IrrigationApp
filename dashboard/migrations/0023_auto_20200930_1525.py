# Generated by Django 2.2.10 on 2020-09-30 13:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0022_auto_20200930_0024'),
    ]

    operations = [
        migrations.AlterField(
            model_name='calendarirrigation',
            name='duration',
            field=models.CharField(choices=[('1 minuto ', '1 minuto '), ('2 minuti ', '2 minuti '), ('3 minuti ', '3 minuti '), ('4 minuti ', '4 minuti '), ('5 minuti ', '5 minuti '), ('6 minuti ', '6 minuti '), ('7 minuti ', '7 minuti '), ('8 minuti ', '8 minuti '), ('9 minuti ', '9 minuti '), ('10 minuti ', '10 minuti '), ('11 minuti ', '11 minuti '), ('12 minuti ', '12 minuti '), ('13 minuti ', '13 minuti '), ('14 minuti ', '14 minuti '), ('15 minuti ', '15 minuti '), ('20 minuti ', '20 minuti '), ('25 minuti ', '25 minuti '), ('30 minuti ', '30 minuti '), ('40 minuti ', '40 minuti '), ('30 minuti ', '30 minuti '), ('45 minuti ', '45 minuti '), ('50 minuti ', '50 minuti '), ('55 minuti ', '55 minuti '), ('60 minuti ', '60 minuti ')], max_length=100, verbose_name='durata'),
        ),
        migrations.AlterField(
            model_name='calendarirrigation',
            name='frequency',
            field=models.CharField(choices=[('0', 'ogni giorno'), ('1', 'giorni alterni'), ('2', 'ogni 2 giorni'), ('3', 'ogni 3 giorni'), ('4', 'ogni 4 giorni'), ('5', 'ogni 5 giorni'), ('7', 'una volta a settimana'), ('10', 'ogni 10 giorni'), ('14', 'una volta ogni due settimane')], default='2', max_length=10, verbose_name='frequenza'),
        ),
    ]
