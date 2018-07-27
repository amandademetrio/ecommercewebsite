# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-07-25 22:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('first_app', '0002_auto_20180724_2115'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='products',
        ),
        migrations.AddField(
            model_name='order',
            name='products',
            field=models.ManyToManyField(related_name='related_orders', to='first_app.Product'),
        ),
    ]
