# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auths', '0005_auto_20160614_2321'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='formatType',
            field=models.CharField(default=b'text', max_length=40, blank=True),
        ),
    ]
