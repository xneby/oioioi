# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2018-08-16 19:12
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contests', '0001_initial'),
        ('contestexcl', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='exclusivenessconfig',
            name='contest',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='contests.Contest'),
        ),
    ]
