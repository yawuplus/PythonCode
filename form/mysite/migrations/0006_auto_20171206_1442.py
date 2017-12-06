# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2017-12-06 06:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0005_delete_about'),
    ]

    operations = [
        migrations.CreateModel(
            name='Letter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=100)),
                ('school', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=100)),
                ('content', models.TextField()),
            ],
        ),
        migrations.DeleteModel(
            name='Person',
        ),
    ]
