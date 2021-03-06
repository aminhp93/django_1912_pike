# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-04 02:54
from __future__ import unicode_literals

import courses.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('categories', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=120)),
                ('slug', models.SlugField(blank=True)),
                ('image', models.ImageField(blank=True, height_field='image_height', null=True, upload_to=courses.models.handle_upload, width_field='image_width')),
                ('image_height', models.IntegerField(blank=True, null=True)),
                ('image_width', models.IntegerField(blank=True, null=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=100)),
                ('active', models.BooleanField(default=True)),
                ('description', models.TextField()),
                ('updated', models.DateTimeField(auto_now=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='primary_category', to='categories.Category')),
                ('secondary', models.ManyToManyField(blank=True, related_name='secondary_category', to='categories.Category')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
