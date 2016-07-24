# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Internal', '0004_employee_additional_position'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=40)),
                ('details', models.TextField()),
                ('video_link', models.URLField()),
                ('photo', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='LiveEventUser',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('phone', models.CharField(unique=True, max_length=10)),
                ('name', models.CharField(max_length=40)),
                ('password', models.CharField(max_length=40)),
            ],
        ),
        migrations.AddField(
            model_name='event',
            name='user',
            field=models.ForeignKey(related_name='eventuser', to='Internal.LiveEventUser'),
        ),
    ]
