# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-06 17:38
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
import shopping.models


class Migration(migrations.Migration):

    dependencies = [
        ('shopping', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='shopping',
            name='image',
            field=models.ImageField(blank=True, height_field='image_height', null=True, upload_to=shopping.models.handle_upload, width_field='image_width'),
        ),
        migrations.AddField(
            model_name='shopping',
            name='image_height',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='shopping',
            name='image_width',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='shopping',
            name='slug',
            field=models.SlugField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
