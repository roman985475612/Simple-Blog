# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-21 10:31
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_post_comments'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='last_comment_date',
            field=models.DateTimeField(default=datetime.datetime(1, 1, 1, 0, 0)),
        ),
    ]