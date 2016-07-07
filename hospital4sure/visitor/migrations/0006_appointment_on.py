# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('visitor', '0005_remove_appointment_on'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='on',
            field=models.DateField(default=datetime.datetime(2016, 7, 6, 13, 44, 31, 484000, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
