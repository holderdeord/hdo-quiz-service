# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-03-04 14:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0008_delete_interim'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='manuscriptitem',
            options={'ordering': ('order',)},
        ),
        migrations.AlterField(
            model_name='manuscriptimage',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
