# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('visitor', '0004_auto_20160706_1848'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appointment',
            name='on',
        ),
    ]
