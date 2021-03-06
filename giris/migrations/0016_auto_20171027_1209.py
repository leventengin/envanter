# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-10-27 09:09
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('giris', '0015_dem_ariza_yparca_ariza_yparca_demirbas'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dem_ariza',
            name='kullanici',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='yparca_ariza',
            name='kullanici',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='yparca_demirbas',
            name='kullanici',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
