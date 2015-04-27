# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('qbdb', '0003_tournament_tournament_year'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bonus',
            old_name='part1_answer_sanitize',
            new_name='part1_answer_sanitized',
        ),
        migrations.RenameField(
            model_name='bonus',
            old_name='part2_answer_sanitize',
            new_name='part2_answer_sanitized',
        ),
        migrations.RenameField(
            model_name='bonus',
            old_name='part3_answer_sanitize',
            new_name='part3_answer_sanitized',
        ),
        migrations.RenameField(
            model_name='bonus',
            old_name='part4_answer_sanitize',
            new_name='part4_answer_sanitized',
        ),
        migrations.RenameField(
            model_name='bonus',
            old_name='part5_answer_sanitize',
            new_name='part5_answer_sanitized',
        ),
        migrations.RenameField(
            model_name='bonus',
            old_name='part6_answer_sanitize',
            new_name='part6_answer_sanitized',
        ),
        migrations.AddField(
            model_name='tossup',
            name='number',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='tournament',
            name='tournament_date',
            field=models.DateField(null=True),
        ),
    ]
