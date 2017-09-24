# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-09-20 15:02
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('giris', '0002_auto_20170918_0802'),
    ]

    operations = [
        migrations.CreateModel(
            name='deneme_giris',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('yazi', models.CharField(max_length=200)),
                ('tarih', models.DateField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
