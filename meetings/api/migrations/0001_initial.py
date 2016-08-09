# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-08-09 07:57
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Conference',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=100)),
                ('site', models.URLField(blank=True)),
                ('city', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=100)),
                ('country', django_countries.fields.CountryField(max_length=2)),
                ('event_start', models.DateTimeField()),
                ('event_end', models.DateTimeField()),
                ('submission_start', models.DateTimeField()),
                ('submission_end', models.DateTimeField()),
                ('logo', models.URLField(blank=True)),
                ('description', models.TextField(blank=True, max_length=500)),
            ],
            options={
                'ordering': ('created',),
            },
        ),
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('node_id', models.CharField(max_length=10)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('approved', models.NullBooleanField()),
                ('conference', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Conference')),
                ('contributors', models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('date_created',),
            },
        ),
    ]
