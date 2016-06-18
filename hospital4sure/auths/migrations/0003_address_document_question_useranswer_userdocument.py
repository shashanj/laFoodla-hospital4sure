# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import auths.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auths', '0002_auto_20160614_0047'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('type', models.CharField(max_length=50)),
                ('state', models.CharField(max_length=50)),
                ('district', models.CharField(max_length=50)),
                ('landmark', models.CharField(max_length=50)),
                ('street', models.CharField(max_length=50)),
                ('pincode', models.CharField(max_length=6)),
                ('user', models.ForeignKey(related_name='address', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('Format', models.CharField(max_length=100)),
                ('MaxSize', models.IntegerField()),
                ('amount', models.IntegerField(default=1)),
                ('category', models.ManyToManyField(to='auths.Category')),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=100)),
                ('options', models.TextField(blank=True)),
                ('type', models.IntegerField()),
                ('require', models.CharField(max_length=10, blank=True)),
                ('placeholder', models.CharField(max_length=40, blank=True)),
                ('order', models.IntegerField(default=0)),
                ('formatType', models.CharField(max_length=40, blank=True)),
                ('category', models.ForeignKey(to='auths.Category')),
                ('subcategory', models.ForeignKey(to='auths.SubCategory')),
            ],
        ),
        migrations.CreateModel(
            name='UserAnswer',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('answer', models.TextField(default=b'')),
                ('question', models.ForeignKey(related_name='questionof', to='auths.Question')),
                ('user', models.ForeignKey(related_name='answerby', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserDocument',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('file', models.FileField(upload_to=auths.models.getfolder)),
                ('documnet', models.ForeignKey(to='auths.Document')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
