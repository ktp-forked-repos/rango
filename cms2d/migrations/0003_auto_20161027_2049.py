# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-10-27 20:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms2d', '0002_topic_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='topic',
            name='description',
            field=models.TextField(default=''),
        ),
    ]
