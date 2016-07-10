# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auths', '0013_auto_20160706_1443'),
    ]

    operations = [
        migrations.CreateModel(
            name='BloodBankUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=60)),
                ('address', models.TextField()),
                ('gpslocation', models.CharField(max_length=30)),
                ('logo', models.URLField()),
                ('city', models.CharField(max_length=100)),
                ('timings', models.TextField()),
                ('password', models.CharField(max_length=100)),
                ('Aplus', models.IntegerField(default=0)),
                ('Aminus', models.IntegerField(default=0)),
                ('Bplus', models.IntegerField(default=0)),
                ('Bminus', models.IntegerField(default=0)),
                ('ABplus', models.IntegerField(default=0)),
                ('ABminus', models.IntegerField(default=0)),
                ('Oplus', models.IntegerField(default=0)),
                ('Ominus', models.IntegerField(default=0)),
                ('ffp', models.IntegerField(default=0)),
                ('plt', models.IntegerField(default=0)),
                ('cry', models.IntegerField(default=0)),
                ('lpl', models.IntegerField(default=0)),
                ('aph', models.IntegerField(default=0)),
                ('unt', models.IntegerField(default=0)),
                ('caplus', models.IntegerField(default=0)),
                ('caminus', models.IntegerField(default=0)),
                ('cbplus', models.IntegerField(default=0)),
                ('cbminus', models.IntegerField(default=0)),
                ('cabplus', models.IntegerField(default=0)),
                ('cabminus', models.IntegerField(default=0)),
                ('coplus', models.IntegerField(default=0)),
                ('cominus', models.IntegerField(default=0)),
                ('update', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(related_name='bloodbank', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
