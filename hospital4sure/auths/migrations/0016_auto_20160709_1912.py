# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auths', '0015_auto_20160709_1906'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bloodbankuser',
            name='ABminus',
            field=models.IntegerField(default=0, verbose_name=b'AB-'),
        ),
        migrations.AlterField(
            model_name='bloodbankuser',
            name='ABplus',
            field=models.IntegerField(default=0, verbose_name=b'AB+'),
        ),
        migrations.AlterField(
            model_name='bloodbankuser',
            name='Aminus',
            field=models.IntegerField(default=0, verbose_name=b'A-'),
        ),
        migrations.AlterField(
            model_name='bloodbankuser',
            name='Bminus',
            field=models.IntegerField(default=0, verbose_name=b'B-'),
        ),
        migrations.AlterField(
            model_name='bloodbankuser',
            name='Bplus',
            field=models.IntegerField(default=0, verbose_name=b'B+'),
        ),
        migrations.AlterField(
            model_name='bloodbankuser',
            name='Ominus',
            field=models.IntegerField(default=0, verbose_name=b'O-'),
        ),
        migrations.AlterField(
            model_name='bloodbankuser',
            name='Oplus',
            field=models.IntegerField(default=0, verbose_name=b'O+'),
        ),
        migrations.AlterField(
            model_name='bloodbankuser',
            name='cabminus',
            field=models.IntegerField(default=0, verbose_name=b'cab-'),
        ),
        migrations.AlterField(
            model_name='bloodbankuser',
            name='cabplus',
            field=models.IntegerField(default=0, verbose_name=b'cab+'),
        ),
        migrations.AlterField(
            model_name='bloodbankuser',
            name='caminus',
            field=models.IntegerField(default=0, verbose_name=b'ca-'),
        ),
        migrations.AlterField(
            model_name='bloodbankuser',
            name='caplus',
            field=models.IntegerField(default=0, verbose_name=b'ca+'),
        ),
        migrations.AlterField(
            model_name='bloodbankuser',
            name='cbminus',
            field=models.IntegerField(default=0, verbose_name=b'cb-'),
        ),
        migrations.AlterField(
            model_name='bloodbankuser',
            name='cbplus',
            field=models.IntegerField(default=0, verbose_name=b'cb+'),
        ),
        migrations.AlterField(
            model_name='bloodbankuser',
            name='cominus',
            field=models.IntegerField(default=0, verbose_name=b'co-'),
        ),
        migrations.AlterField(
            model_name='bloodbankuser',
            name='coplus',
            field=models.IntegerField(default=0, verbose_name=b'co+'),
        ),
    ]
