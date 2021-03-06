# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-01 04:55
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('qbdb', '0012_auto_20150511_2117'),
    ]

    operations = [
        migrations.CreateModel(
            name='BonusPart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('answer', models.TextField()),
                ('value', models.IntegerField()),
                ('text_sanitized', models.TextField()),
                ('answer_sanitized', models.TextField()),
            ],
        ),
        migrations.RemoveField(
            model_name='bonus',
            name='part1_answer',
        ),
        migrations.RemoveField(
            model_name='bonus',
            name='part1_answer_sanitized',
        ),
        migrations.RemoveField(
            model_name='bonus',
            name='part1_text',
        ),
        migrations.RemoveField(
            model_name='bonus',
            name='part1_text_sanitized',
        ),
        migrations.RemoveField(
            model_name='bonus',
            name='part1_value',
        ),
        migrations.RemoveField(
            model_name='bonus',
            name='part2_answer',
        ),
        migrations.RemoveField(
            model_name='bonus',
            name='part2_answer_sanitized',
        ),
        migrations.RemoveField(
            model_name='bonus',
            name='part2_text',
        ),
        migrations.RemoveField(
            model_name='bonus',
            name='part2_text_sanitized',
        ),
        migrations.RemoveField(
            model_name='bonus',
            name='part2_value',
        ),
        migrations.RemoveField(
            model_name='bonus',
            name='part3_answer',
        ),
        migrations.RemoveField(
            model_name='bonus',
            name='part3_answer_sanitized',
        ),
        migrations.RemoveField(
            model_name='bonus',
            name='part3_text',
        ),
        migrations.RemoveField(
            model_name='bonus',
            name='part3_text_sanitized',
        ),
        migrations.RemoveField(
            model_name='bonus',
            name='part3_value',
        ),
        migrations.RemoveField(
            model_name='bonus',
            name='part4_answer',
        ),
        migrations.RemoveField(
            model_name='bonus',
            name='part4_answer_sanitized',
        ),
        migrations.RemoveField(
            model_name='bonus',
            name='part4_text',
        ),
        migrations.RemoveField(
            model_name='bonus',
            name='part4_text_sanitized',
        ),
        migrations.RemoveField(
            model_name='bonus',
            name='part4_value',
        ),
        migrations.RemoveField(
            model_name='bonus',
            name='part5_answer',
        ),
        migrations.RemoveField(
            model_name='bonus',
            name='part5_answer_sanitized',
        ),
        migrations.RemoveField(
            model_name='bonus',
            name='part5_text',
        ),
        migrations.RemoveField(
            model_name='bonus',
            name='part5_text_sanitized',
        ),
        migrations.RemoveField(
            model_name='bonus',
            name='part5_value',
        ),
        migrations.RemoveField(
            model_name='bonus',
            name='part6_answer',
        ),
        migrations.RemoveField(
            model_name='bonus',
            name='part6_answer_sanitized',
        ),
        migrations.RemoveField(
            model_name='bonus',
            name='part6_text',
        ),
        migrations.RemoveField(
            model_name='bonus',
            name='part6_text_sanitized',
        ),
        migrations.RemoveField(
            model_name='bonus',
            name='part6_value',
        ),
        migrations.AddField(
            model_name='bonuspart',
            name='bonus',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='qbdb.Bonus'),
        ),
    ]
