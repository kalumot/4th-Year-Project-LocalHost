# Generated by Django 2.1.4 on 2019-02-18 10:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ammamanager', '0002_auto_20190211_1233'),
    ]

    operations = [
        migrations.AddField(
            model_name='fighter',
            name='weight',
            field=models.CharField(choices=[('FLW', 'Flyweight'), ('BW', 'Bantamweight'), ('FW', 'Featherweight'), ('LW', 'Lightweight')], default='FLW', max_length=1),
        ),
    ]