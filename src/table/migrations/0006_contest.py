# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-12-30 11:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('table', '0005_card_level'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('login_regex', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('cards', models.ManyToManyField(related_name='_contest_cards_+', to='table.Card')),
            ],
        ),
    ]
