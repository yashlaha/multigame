# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-06-20 19:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0003_auto_20160621_0055'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='id',
            field=models.AutoField(auto_created=True, default=0, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='game',
            name='gameid',
            field=models.IntegerField(),
        ),
    ]
