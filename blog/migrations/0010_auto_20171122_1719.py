# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-22 17:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_post_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='rating',
            field=models.SmallIntegerField(default=0),
        ),
    ]