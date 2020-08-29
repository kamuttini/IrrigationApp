# Generated by Django 2.2.10 on 2020-08-29 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0008_auto_20200828_0956'),
    ]

    operations = [
        migrations.AddField(
            model_name='garden',
            name='image',
            field=models.CharField(choices=[('cover/balcony.jpg', 'Plant'), ('cover/terrace.jpg', 'Tree'), ('cover/garden.jpg', 'Garden'), ('cover/vegetable.jpg', 'Vegetable'), ('cover/flower.jpg', 'Flower')], default='cover/balcony.jpg', max_length=255),
        ),
    ]
