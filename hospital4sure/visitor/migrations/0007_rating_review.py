# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('visitor', '0006_appointment_on'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('amount', models.IntegerField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('by', models.ForeignKey(related_name='byuser', to=settings.AUTH_USER_MODEL)),
                ('of', models.ForeignKey(related_name='ofuser', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('text', models.TextField()),
                ('active', models.BooleanField(default=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('by', models.ForeignKey(related_name='reviewbyuser', to=settings.AUTH_USER_MODEL)),
                ('of', models.ForeignKey(related_name='reviewofuser', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
