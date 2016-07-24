# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('visitor', '0008_temporarybloodbankvisitor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='temporarybloodbankvisitor',
            name='phone_numeber',
            field=models.CharField(unique=True, max_length=18),
        ),
    ]
