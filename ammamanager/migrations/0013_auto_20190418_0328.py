# Generated by Django 2.1.3 on 2019-04-18 02:28

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ammamanager', '0012_auto_20190418_0223'),
    ]

    operations = [
        migrations.AddField(
            model_name='bout',
            name='completed',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='event',
            name='date',
            field=models.DateField(default=datetime.datetime(2019, 4, 18, 3, 28, 14, 719829)),
        ),
    ]