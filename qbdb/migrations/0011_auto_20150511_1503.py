# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('qbdb', '0010_auto_20150511_0052'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bonus',
            old_name='rating',
            new_name='quality',
        ),
        migrations.RenameField(
            model_name='packet',
            old_name='rating',
            new_name='quality',
        ),
        migrations.RenameField(
            model_name='tossup',
            old_name='rating',
            new_name='quality',
        ),
        migrations.RenameField(
            model_name='tournament',
            old_name='rating',
            new_name='quality',
        ),
    ]
