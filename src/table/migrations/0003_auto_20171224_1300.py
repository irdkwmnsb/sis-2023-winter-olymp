# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-12-24 13:00
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('table', '0002_cardstatus'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cardstatus',
            name='card',
        ),
        migrations.RemoveField(
            model_name='cardstatus',
            name='user',
        ),
        migrations.DeleteModel(
            name='CardStatus',
        ),
    ]
