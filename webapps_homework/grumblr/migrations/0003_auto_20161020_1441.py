# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-20 18:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grumblr', '0002_auto_20161020_1440'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='time',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
