# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auths', '0010_document_list_view'),
    ]

    operations = [
        migrations.CreateModel(
            name='DisplayCategory',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(default=b'', max_length=250)),
            ],
        ),
    ]
