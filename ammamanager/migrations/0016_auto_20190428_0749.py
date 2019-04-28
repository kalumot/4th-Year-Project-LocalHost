# Generated by Django 2.1.3 on 2019-04-28 06:49

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ammamanager', '0015_auto_20190428_0435'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='date',
            field=models.DateField(default=datetime.datetime(2019, 4, 28, 7, 49, 0, 516368)),
        ),
        migrations.AlterField(
            model_name='fighter',
            name='createDate',
            field=models.DateField(default=datetime.datetime(2019, 4, 28, 7, 49, 0, 517869)),
        ),
        migrations.AlterField(
            model_name='fighter',
            name='gym',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='fighters', to=settings.AUTH_USER_MODEL),
        ),
    ]
