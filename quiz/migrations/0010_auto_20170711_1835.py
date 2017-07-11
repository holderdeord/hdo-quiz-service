# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-11 18:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0009_auto_20170711_1240'),
    ]

    operations = [
        migrations.AlterField(
            model_name='manuscript',
            name='name',
            field=models.CharField(blank=True, default='', help_text='Used both for admin display and user display when type=voting guide', max_length=255, unique=True),
        ),
        migrations.AlterUniqueTogether(
            name='voterguidealternative',
            unique_together=set([('text', 'manuscript')]),
        ),
    ]
