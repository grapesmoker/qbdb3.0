# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('qbdb', '0005_auto_20150427_1516'),
    ]

    operations = [
        migrations.AddField(
            model_name='bonus',
            name='number',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
