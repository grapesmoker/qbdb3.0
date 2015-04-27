# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bonus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('leadin', models.TextField()),
                ('leadin_sanitized', models.TextField()),
                ('part1_text', models.TextField()),
                ('part1_answer', models.TextField()),
                ('part1_value', models.IntegerField()),
                ('part1_text_sanitized', models.TextField()),
                ('part1_answer_sanitize', models.TextField()),
                ('part2_text', models.TextField()),
                ('part2_answer', models.TextField()),
                ('part2_value', models.IntegerField()),
                ('part2_text_sanitized', models.TextField()),
                ('part2_answer_sanitize', models.TextField()),
                ('part3_text', models.TextField()),
                ('part3_answer', models.TextField()),
                ('part3_value', models.IntegerField()),
                ('part3_text_sanitized', models.TextField()),
                ('part3_answer_sanitize', models.TextField()),
                ('part4_text', models.TextField()),
                ('part4_answer', models.TextField()),
                ('part4_value', models.IntegerField()),
                ('part4_text_sanitized', models.TextField()),
                ('part4_answer_sanitize', models.TextField()),
                ('part5_text', models.TextField()),
                ('part5_answer', models.TextField()),
                ('part5_value', models.IntegerField()),
                ('part5_text_sanitized', models.TextField()),
                ('part5_answer_sanitize', models.TextField()),
                ('part6_text', models.TextField()),
                ('part6_answer', models.TextField()),
                ('part6_value', models.IntegerField()),
                ('part6_text_sanitized', models.TextField()),
                ('part6_answer_sanitize', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Tossup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tossup_text', models.TextField()),
                ('tossup_text_sanitized', models.TextField()),
                ('answer', models.TextField()),
                ('answer_sanitized', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Tournament',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tournament_name', models.CharField(max_length=250)),
                ('tournament_date', models.DateField()),
            ],
        ),
        migrations.AddField(
            model_name='tossup',
            name='tournament',
            field=models.ForeignKey(to='qbdb.Tournament'),
        ),
        migrations.AddField(
            model_name='bonus',
            name='tournament',
            field=models.ForeignKey(to='qbdb.Tournament'),
        ),
    ]
