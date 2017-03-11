# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-11 03:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartitem',
            name='user',
        ),
        migrations.AlterField(
            model_name='cart',
            name='tax_percentage',
            field=models.DecimalField(decimal_places=2, default=0.08, max_digits=50),
        ),
    ]
