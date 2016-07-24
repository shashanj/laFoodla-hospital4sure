# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auths', '0016_auto_20160709_1912'),
    ]

    operations = [
        migrations.AddField(
            model_name='bloodbankuser',
            name='registration_number',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
    ]
