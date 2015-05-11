# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('qbdb', '0011_auto_20150511_1503'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bonusvote',
            old_name='packet',
            new_name='bonus',
        ),
        migrations.RenameField(
            model_name='tossupvote',
            old_name='packet',
            new_name='tossup',
        ),
    ]
