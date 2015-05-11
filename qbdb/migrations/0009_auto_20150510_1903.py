# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('qbdb', '0008_auto_20150510_1900'),
    ]

    operations = [
        migrations.AddField(
            model_name='qbdbuser',
            name='bonus_diff',
            field=models.ManyToManyField(related_name='bonus_diff', to='qbdb.Bonus'),
        ),
        migrations.AddField(
            model_name='qbdbuser',
            name='bonus_quality',
            field=models.ManyToManyField(related_name='bonus_quality', to='qbdb.Bonus'),
        ),
        migrations.AddField(
            model_name='qbdbuser',
            name='packet_diff',
            field=models.ManyToManyField(related_name='packet_diff', to='qbdb.Packet'),
        ),
        migrations.AddField(
            model_name='qbdbuser',
            name='packet_quality',
            field=models.ManyToManyField(related_name='packet_quality', to='qbdb.Packet'),
        ),
        migrations.AddField(
            model_name='qbdbuser',
            name='tossup_diff',
            field=models.ManyToManyField(related_name='tossup_diff', to='qbdb.Tossup'),
        ),
        migrations.AddField(
            model_name='qbdbuser',
            name='tossup_quality',
            field=models.ManyToManyField(related_name='tossup_quality', to='qbdb.Tossup'),
        ),
        migrations.AddField(
            model_name='qbdbuser',
            name='tournament_diff',
            field=models.ManyToManyField(related_name='tour_diff', to='qbdb.Tournament'),
        ),
        migrations.AddField(
            model_name='qbdbuser',
            name='tournament_quality',
            field=models.ManyToManyField(related_name='tour_quality', to='qbdb.Tournament'),
        ),
    ]
