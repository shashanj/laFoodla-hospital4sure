# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('Internal', '0005_auto_20160724_1537'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2016, 7, 24, 10, 12, 35, 912000, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
    ]
