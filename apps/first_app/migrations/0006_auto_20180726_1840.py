# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-07-26 18:40
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('first_app', '0005_remove_order_total_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='billing_zipcode',
        ),
        migrations.RemoveField(
            model_name='user',
            name='shipping_zipcode',
        ),
    ]
