# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auths', '0012_question_disp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='disp',
            field=models.ManyToManyField(to='auths.DisplayCategory', blank=True),
        ),
    ]
