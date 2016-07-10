# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auths', '0014_bloodbankuser'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bloodbankuser',
            name='Aplus',
            field=models.IntegerField(default=0, verbose_name=b'A+'),
        ),
    ]
