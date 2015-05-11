# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('qbdb', '0009_auto_20150510_1903'),
    ]

    operations = [
        migrations.CreateModel(
            name='BonusVote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('difficulty', models.FloatField(default=0.0)),
                ('quality', models.FloatField(default=0.0)),
                ('packet', models.ForeignKey(to='qbdb.Bonus')),
            ],
        ),
        migrations.CreateModel(
            name='PacketVote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('difficulty', models.FloatField(default=0.0)),
                ('quality', models.FloatField(default=0.0)),
                ('packet', models.ForeignKey(to='qbdb.Packet')),
            ],
        ),
        migrations.CreateModel(
            name='TossupVote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('difficulty', models.FloatField(default=0.0)),
                ('quality', models.FloatField(default=0.0)),
                ('packet', models.ForeignKey(to='qbdb.Tossup')),
            ],
        ),
        migrations.CreateModel(
            name='TournamentVote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('difficulty', models.FloatField(default=0.0)),
                ('quality', models.FloatField(default=0.0)),
                ('tournament', models.ForeignKey(to='qbdb.Tournament')),
            ],
        ),
        migrations.RemoveField(
            model_name='qbdbuser',
            name='bonus_diff',
        ),
        migrations.RemoveField(
            model_name='qbdbuser',
            name='bonus_quality',
        ),
        migrations.RemoveField(
            model_name='qbdbuser',
            name='packet_diff',
        ),
        migrations.RemoveField(
            model_name='qbdbuser',
            name='packet_quality',
        ),
        migrations.RemoveField(
            model_name='qbdbuser',
            name='tossup_diff',
        ),
        migrations.RemoveField(
            model_name='qbdbuser',
            name='tossup_quality',
        ),
        migrations.RemoveField(
            model_name='qbdbuser',
            name='tournament_diff',
        ),
        migrations.RemoveField(
            model_name='qbdbuser',
            name='tournament_quality',
        ),
        migrations.AddField(
            model_name='tournamentvote',
            name='user',
            field=models.ForeignKey(to='qbdb.QBDBUser'),
        ),
        migrations.AddField(
            model_name='tossupvote',
            name='user',
            field=models.ForeignKey(to='qbdb.QBDBUser'),
        ),
        migrations.AddField(
            model_name='packetvote',
            name='user',
            field=models.ForeignKey(to='qbdb.QBDBUser'),
        ),
        migrations.AddField(
            model_name='bonusvote',
            name='user',
            field=models.ForeignKey(to='qbdb.QBDBUser'),
        ),
        migrations.AddField(
            model_name='qbdbuser',
            name='bonus',
            field=models.ManyToManyField(to='qbdb.Bonus', through='qbdb.BonusVote'),
        ),
        migrations.AddField(
            model_name='qbdbuser',
            name='packet',
            field=models.ManyToManyField(to='qbdb.Packet', through='qbdb.PacketVote'),
        ),
        migrations.AddField(
            model_name='qbdbuser',
            name='tossup',
            field=models.ManyToManyField(to='qbdb.Tossup', through='qbdb.TossupVote'),
        ),
        migrations.AddField(
            model_name='qbdbuser',
            name='tournament',
            field=models.ManyToManyField(to='qbdb.Tournament', through='qbdb.TournamentVote'),
        ),
    ]
