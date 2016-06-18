# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(default=b' ', max_length=250)),
                ('membershhip_fees', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='SubCategory',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(default=b' ', max_length=250)),
                ('category', models.ForeignKey(to='auths.Category')),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=50)),
                ('register', models.IntegerField(default=b'0')),
                ('verfied', models.IntegerField(default=b'0')),
                ('telephone', models.CharField(max_length=13)),
                ('username', models.CharField(unique=True, max_length=13)),
                ('website', models.URLField()),
                ('category', models.ForeignKey(related_name='category', to='auths.Category')),
                ('subcategory', models.ForeignKey(related_name='sub_Category', blank=True, to='auths.SubCategory', null=True)),
                ('user', models.OneToOneField(related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
