# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('qbdb', '0002_auto_20150425_1853'),
    ]

    operations = [
        migrations.AddField(
            model_name='tournament',
            name='tournament_year',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
