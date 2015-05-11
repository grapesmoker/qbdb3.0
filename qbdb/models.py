from django.db import models
from django.contrib.auth.models import User

import json
# Create your models here.

class Tossup(models.Model):

    tossup_text = models.TextField()
    tossup_text_sanitized = models.TextField()
    answer = models.TextField()
    answer_sanitized = models.TextField()
    number = models.IntegerField()

    packet = models.ForeignKey('Packet', null=True)
    tournament = models.ForeignKey('Tournament')

    quality = models.FloatField(default=0)
    difficulty = models.FloatField(default=0)

    def to_dict(self, user=None):

        data = {'tossup_text': self.tossup_text,
                'answer': self.answer,
                'number': self.number,
                'id': self.id,
                'packet_name': self.packet.author,
                'packet_id': self.packet.id,
                'tournament': self.tournament.tournament_name,
                'tournament_id': self.tournament.id,
                'year': self.tournament.tournament_year,
                'difficulty': self.difficulty,
                'quality': self.quality}

        if user:
            vote = self.tossupvote_set.filter(user=user).first()
            if vote:
                data['my_diff'] = vote.difficulty
                data['my_qual'] = vote.quality
            else:
                data['my_diff'] = 0
                data['my_qual'] = 0
        else:
            data['my_diff'] = 0
            data['my_qual'] = 0

        return data

    def to_json(self, user=None):

        return json.dumps(self.to_dict(user=user))

class Bonus(models.Model):

    leadin = models.TextField()
    leadin_sanitized = models.TextField()

    number = models.IntegerField()

    part1_text = models.TextField()
    part1_answer = models.TextField()
    part1_value = models.IntegerField()
    part1_text_sanitized = models.TextField()
    part1_answer_sanitized = models.TextField()

    part2_text = models.TextField(default='')
    part2_answer = models.TextField(default='')
    part2_value = models.IntegerField(default=0)
    part2_text_sanitized = models.TextField(default='')
    part2_answer_sanitized = models.TextField(default='')

    part3_text = models.TextField(default='')
    part3_answer = models.TextField(default='')
    part3_value = models.IntegerField(default=0)
    part3_text_sanitized = models.TextField(default='')
    part3_answer_sanitized = models.TextField(default='')

    part4_text = models.TextField(default='')
    part4_answer = models.TextField(default='')
    part4_value = models.IntegerField(default=0)
    part4_text_sanitized = models.TextField(default='')
    part4_answer_sanitized = models.TextField(default='')

    part5_text = models.TextField(default='')
    part5_answer = models.TextField(default='')
    part5_value = models.IntegerField(default=0)
    part5_text_sanitized = models.TextField(default='')
    part5_answer_sanitized = models.TextField(default='')

    part6_text = models.TextField(default='')
    part6_answer = models.TextField(default='')
    part6_value = models.IntegerField(default=0)
    part6_text_sanitized = models.TextField(default='')
    part6_answer_sanitized = models.TextField(default='')

    packet = models.ForeignKey('Packet', null=True)
    tournament = models.ForeignKey('Tournament')

    quality = models.FloatField(default=0)
    difficulty = models.FloatField(default=0)

    def to_dict(self, user=None):
        data = {'leadin': self.leadin,
                'id': self.id,
                'number': self.number,
                'packet_name': self.packet.author,
                'packet_id': self.packet.id,
                'tournament': self.tournament.tournament_name,
                'tournament_id': self.tournament.id,
                'year': self.tournament.tournament_year,
                'difficulty': self.difficulty,
                'quality': self.quality,
                'values': [],
                'parts': [],
                'answers': []}

        fields = [('text', 'parts'), ('answer', 'answers'), ('value', 'values')]
        for i in range(1, 7):
            for f in fields:
                field = 'part{0}_{1}'.format(i, f[0])
                data[f[1]].append(getattr(self, field))

        if user:
            vote = self.bonusvote_set.filter(user=user).first()
            if vote:
                data['my_diff'] = vote.difficulty
                data['my_qual'] = vote.quality
            else:
                data['my_diff'] = 0
                data['my_qual'] = 0
        else:
            data['my_diff'] = 0
            data['my_qual'] = 0

        return data

    def to_json(self, user=None):
        return json.dumps(self.to_dict(user=user))


class Packet(models.Model):

    tournament = models.ForeignKey('Tournament')
    author = models.CharField(max_length=250)

    quality = models.FloatField(default=0)
    difficulty = models.FloatField(default=0)

    def to_dict(self, with_questions=False, user=None):
        data = {}
        if with_questions:
            data['tossups'] = [tossup.to_dict(user=user) for tossup in self.tossup_set.all()]
            data['bonuses'] = [bonus.to_dict(user=user) for bonus in self.bonus_set.all()]

        data['author'] = self.author
        data['tournament'] = self.tournament.tournament_name
        data['tournament_id'] = self.tournament.id
        data['id'] = self.id
        data['year'] = self.tournament.tournament_year
        data['difficulty'] = self.difficulty
        data['quality'] = self.quality

        if user:
            vote = self.packetvote_set.filter(user=user).first()
            if vote:
                data['my_diff'] = vote.difficulty
                data['my_qual'] = vote.quality

        return data

    def to_json(self, with_questions=False, user=None):
        return json.dumps(self.to_dict(with_questions, user))

class Tournament(models.Model):

    tournament_name = models.CharField(max_length=250)
    tournament_date = models.DateField(null=True)
    tournament_year = models.IntegerField()

    quality = models.FloatField(default=0)
    difficulty = models.FloatField(default=0)

    def to_dict(self, with_packets=False, user=None):
        data = {}
        if with_packets:
            packets = [packet.to_dict(user=user) for packet in self.packet_set.all()]
            data['packets'] = packets

        data['tournament_name'] = self.tournament_name
        data['tournament_year'] = self.tournament_year
        data['id'] = self.id
        data['difficulty'] = self.difficulty
        data['quality'] = self.quality

        if user:
            vote = self.tournamentvote_set.filter(user=user).first()
            if vote:
                data['my_diff'] = vote.difficulty
                data['my_qual'] = vote.quality

        return data


    def to_json(self, with_packets=False, user=None):
        return json.dumps(self.to_dict(with_packets, user))


class QBDBUser(models.Model):

    user = models.OneToOneField(User)

    affiliation = models.CharField(max_length=250)

    # voting fields for tournament, packet, tossup, and bonus

    tournament = models.ManyToManyField('Tournament', through='TournamentVote')
    packet = models.ManyToManyField('Packet', through='PacketVote')
    tossup = models.ManyToManyField('Tossup', through='TossupVote')
    bonus = models.ManyToManyField('Bonus', through='BonusVote')

    def __str__(self):
        return '{0!s} {1!s} ({2!s})'.format(self.user.first_name, self.user.last_name, self.user.username)

class TournamentVote(models.Model):

    user = models.ForeignKey(QBDBUser)
    tournament = models.ForeignKey(Tournament)
    difficulty = models.FloatField(default=0.0)
    quality = models.FloatField(default=0.0)

class PacketVote(models.Model):

    user = models.ForeignKey(QBDBUser)
    packet = models.ForeignKey(Packet)
    difficulty = models.FloatField(default=0.0)
    quality = models.FloatField(default=0.0)


class TossupVote(models.Model):

    user = models.ForeignKey(QBDBUser)
    tossup = models.ForeignKey(Tossup)
    difficulty = models.FloatField(default=0.0)
    quality = models.FloatField(default=0.0)

class BonusVote(models.Model):

    user = models.ForeignKey(QBDBUser)
    bonus = models.ForeignKey(Bonus)
    difficulty = models.FloatField(default=0.0)
    quality = models.FloatField(default=0.0)
