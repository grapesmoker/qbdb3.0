# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('qbdb', '0007_qbdbuser'),
    ]

    operations = [
        migrations.AddField(
            model_name='bonus',
            name='difficulty',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='bonus',
            name='rating',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='packet',
            name='difficulty',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='packet',
            name='rating',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='tossup',
            name='difficulty',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='tossup',
            name='rating',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='tournament',
            name='difficulty',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='tournament',
            name='rating',
            field=models.FloatField(default=0),
        ),
    ]
