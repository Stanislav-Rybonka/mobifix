# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-12-25 15:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0002_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('unconfirmed', 'Unconfirmed'), ('pending', 'Pending'), ('completed', 'Completed'), ('returned', 'Returned')], default='unconfirmed', max_length=50, verbose_name='status'),
        ),
    ]
