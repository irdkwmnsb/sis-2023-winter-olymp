# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-12-30 15:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('table', '0008_auto_20171230_1154'),
    ]

    operations = [
        migrations.AddField(
            model_name='country',
            name='bonus',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
    ]
