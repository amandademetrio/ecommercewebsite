# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-07-26 21:13
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('first_app', '0008_auto_20180726_2111'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='category',
        ),
        migrations.DeleteModel(
            name='Category',
        ),
    ]