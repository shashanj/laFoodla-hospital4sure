# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Internal', '0003_auto_20160724_1258'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='additional_position',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
    ]
