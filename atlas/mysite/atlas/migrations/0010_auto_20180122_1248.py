# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-01-22 07:18
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('atlas', '0009_auto_20180122_1243'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='uploadanalyses',
            name='rid',
        ),
        migrations.DeleteModel(
            name='Uploads',
        ),
        migrations.DeleteModel(
            name='UploadAnalyses',
        ),
    ]
