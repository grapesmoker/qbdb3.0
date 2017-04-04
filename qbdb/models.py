from django.db import models
from django.contrib.auth.models import User


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

    @property
    def tournament_name(self):
        return self.tournament.tournament_name

    @property
    def tour_id(self):
        return self.tournament.id

    @property
    def author(self):
        return self.packet.author

    @property
    def pack_id(self):
        return self.packet.id


class Bonus(models.Model):

    leadin = models.TextField()
    leadin_sanitized = models.TextField()

    number = models.IntegerField()

    packet = models.ForeignKey('Packet', null=True)
    tournament = models.ForeignKey('Tournament')

    quality = models.FloatField(default=0)
    difficulty = models.FloatField(default=0)

    @property
    def tournament_name(self):
        return self.tournament.tournament_name

    @property
    def tour_id(self):
        return self.tournament.id

    @property
    def author(self):
        return self.packet.author

    @property
    def pack_id(self):
        return self.packet.id


class BonusPart(models.Model):

    text = models.TextField()
    answer = models.TextField()
    value = models.IntegerField()
    text_sanitized = models.TextField()
    answer_sanitized = models.TextField()

    bonus = models.ForeignKey('Bonus')


class Packet(models.Model):

    tournament = models.ForeignKey('Tournament')
    author = models.CharField(max_length=250)

    quality = models.FloatField(default=0)
    difficulty = models.FloatField(default=0)

    @property
    def tournament_name(self):
        return self.tournament.tournament_name

    @property
    def tour_id(self):
        return self.tournament.id


class Tournament(models.Model):

    tournament_name = models.CharField(max_length=250)
    tournament_date = models.DateField(null=True)
    tournament_year = models.IntegerField()

    quality = models.FloatField(default=0)
    difficulty = models.FloatField(default=0)

    @property
    def packets(self):
        return [{'id': packet.id, 'author': packet.author} for packet in self.packet_set.all()]


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
