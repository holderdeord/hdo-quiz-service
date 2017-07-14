# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-14 13:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0010_auto_20170711_1835'),
    ]

    operations = [
        migrations.AddField(
            model_name='manuscript',
            name='is_first_in_category',
            field=models.BooleanField(default=False, help_text='Which manuscript in a category comes first (used with TYPE_VG_CATEGORY_SELECT)'),
        ),
        migrations.AlterField(
            model_name='answer',
            name='answer',
            field=models.CharField(blank=True, choices=[('agree', 'Agrees'), ('disagree', 'Disagrees')], default='', help_text='Used with voting guide', max_length=255),
        ),
    ]