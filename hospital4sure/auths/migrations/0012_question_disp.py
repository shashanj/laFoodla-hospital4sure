# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auths', '0011_displaycategory'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='disp',
            field=models.ManyToManyField(to='auths.DisplayCategory'),
        ),
    ]
