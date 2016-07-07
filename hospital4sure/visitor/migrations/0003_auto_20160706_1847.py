# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('visitor', '0002_appointment'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='comment',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='service',
            field=models.CharField(max_length=100, blank=True),
        ),
    ]
