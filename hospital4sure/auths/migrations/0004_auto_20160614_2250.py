# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auths', '0003_address_document_question_useranswer_userdocument'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='category',
        ),
        migrations.AddField(
            model_name='question',
            name='category',
            field=models.ManyToManyField(to='auths.Category'),
        ),
        migrations.RemoveField(
            model_name='question',
            name='subcategory',
        ),
        migrations.AddField(
            model_name='question',
            name='subcategory',
            field=models.ManyToManyField(to='auths.SubCategory'),
        ),
    ]
