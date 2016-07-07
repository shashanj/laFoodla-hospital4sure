# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('visitor', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('on', models.DateField()),
                ('specialization', models.CharField(max_length=100)),
                ('service', models.CharField(max_length=100)),
                ('time', models.TimeField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('appointmentwith', models.ForeignKey(related_name='appointmentwith', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(related_name='by', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
