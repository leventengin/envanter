# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-10-27 11:25
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('giris', '0016_auto_20171027_1209'),
    ]

    operations = [
        migrations.AddField(
            model_name='dem_ariza',
            name='alt_kategori',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='giris.alt_kategori'),
            preserve_default=False,
        ),
    ]
