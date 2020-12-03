# Generated by Django 2.2.10 on 2020-12-03 10:11

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0037_auto_20201202_1840'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rain',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start', models.DateTimeField(default=django.utils.timezone.now)),
                ('end', models.DateTimeField(blank=True, null=True)),
                ('garden', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='dashboard.Garden')),
            ],
        ),
    ]