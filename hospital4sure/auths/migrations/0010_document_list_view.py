# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auths', '0009_auto_20160621_2323'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='list_view',
            field=models.IntegerField(default=0),
        ),
    ]
