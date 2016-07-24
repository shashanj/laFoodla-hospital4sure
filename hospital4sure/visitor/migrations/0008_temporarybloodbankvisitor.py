# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('visitor', '0007_rating_review'),
    ]

    operations = [
        migrations.CreateModel(
            name='TemporaryBloodbankVisitor',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=40)),
                ('email', models.EmailField(max_length=254, blank=True)),
                ('phone_numeber', models.CharField(unique=True, max_length=13)),
            ],
        ),
    ]
