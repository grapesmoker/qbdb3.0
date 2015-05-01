from django.db import models

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

    def to_dict(self):

        return {'tossup_text': self.tossup_text,
                'answer': self.answer,
                'number': self.number,
                'id': self.id}

    def to_json(self):

        return json.dumps(self.to_dict())

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

    def to_dict(self):
        data = {'leadin': self.leadin,
                'id': self.id,
                'number': self.number,
                'values': [],
                'parts': [],
                'answers': []}

        fields = [('text', 'parts'), ('answer', 'answers'), ('value', 'values')]
        for i in range(1, 7):
            for f in fields:
                field = 'part{0}_{1}'.format(i, f[0])
                data[f[1]].append(getattr(self, field))

        print data

        return data

    def to_json(self):
        return json.dumps(self.to_dict())


class Packet(models.Model):

    tournament = models.ForeignKey('Tournament')
    author = models.CharField(max_length=250)

    def to_dict(self, with_questions=False):
        data = {}
        if with_questions:
            data['tossups'] = [tossup.to_dict() for tossup in self.tossup_set.all()]
            data['bonuses'] = [bonus.to_dict() for bonus in self.bonus_set.all()]

        data['author'] = self.author
        data['tournament'] = self.tournament.tournament_name
        data['tournament_id'] = self.tournament.id
        data['id'] = self.id

        return data

    def to_json(self, with_questions=False):
        return json.dumps(self.to_dict(with_questions))

class Tournament(models.Model):

    tournament_name = models.CharField(max_length=250)
    tournament_date = models.DateField(null=True)
    tournament_year = models.IntegerField()

    def to_dict(self, with_packets=False):
        data = {}
        if with_packets:
            packets = [packet.to_dict() for packet in self.packet_set.all()]
            data['packets'] = packets

        data['tournament_name'] = self.tournament_name
        data['tournament_year'] = self.tournament_year
        data['id'] = self.id

        return data


    def to_json(self, with_packets=False):
        return json.dumps(self.to_dict(with_packets))
