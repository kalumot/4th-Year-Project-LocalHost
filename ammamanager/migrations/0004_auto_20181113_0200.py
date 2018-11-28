# Generated by Django 2.0.1 on 2018-11-13 02:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ammamanager', '0003_fighter'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fighter',
            name='gym',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fighters', to=settings.AUTH_USER_MODEL),
        ),
    ]