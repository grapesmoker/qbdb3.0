# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('qbdb', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Packet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('author', models.CharField(max_length=250)),
                ('tournament', models.ForeignKey(to='qbdb.Tournament')),
            ],
        ),
        migrations.AddField(
            model_name='bonus',
            name='packet',
            field=models.ForeignKey(to='qbdb.Packet', null=True),
        ),
        migrations.AddField(
            model_name='tossup',
            name='packet',
            field=models.ForeignKey(to='qbdb.Packet', null=True),
        ),
    ]
