# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-12-31 08:18
from __future__ import unicode_literals

from django.db import migrations, models
import table.models


class Migration(migrations.Migration):

    dependencies = [
        ('table', '0012_card_photo_id_squashed_0015_card_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='resource',
            name='gender',
            field=models.PositiveIntegerField(choices=[(0, 'Male'), (2, 'Female'), (3, 'Neuter')], default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='resource',
            name='color',
            field=models.CharField(help_text='blue, yellow, red или green', max_length=10),
        ),
    ]
