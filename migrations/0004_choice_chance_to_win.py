# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-07 07:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('infomarket', '0003_choice_total_bet'),
    ]

    operations = [
        migrations.AddField(
            model_name='choice',
            name='chance_to_win',
            field=models.FloatField(default=0),
        ),
    ]
