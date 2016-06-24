# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auths', '0008_address_city'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdocument',
            name='user',
            field=models.ForeignKey(related_name='docsof', to=settings.AUTH_USER_MODEL),
        ),
    ]
