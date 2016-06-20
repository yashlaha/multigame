# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-06-17 21:13
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('gameid', models.AutoField(primary_key=True, serialize=False)),
                ('square', models.IntegerField()),
                ('no_of_player', models.IntegerField(default=0)),
                ('is_active', models.BooleanField(default=False)),
                ('is_completed', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('userid', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=200)),
                ('color', models.CharField(max_length=200)),
            ],
        ),
        migrations.AddField(
            model_name='game',
            name='challenge',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.UserProfile'),
        ),
    ]
