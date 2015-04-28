from django.db import models

# Create your models here.

class Tossup(models.Model):

    tossup_text = models.TextField()
    tossup_text_sanitized = models.TextField()
    answer = models.TextField()
    answer_sanitized = models.TextField()
    number = models.IntegerField()

    packet = models.ForeignKey('Packet', null=True)
    tournament = models.ForeignKey('Tournament')


class Bonus(models.Model):

    leadin = models.TextField()
    leadin_sanitized = models.TextField()

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

class Packet(models.Model):

    tournament = models.ForeignKey('Tournament')
    author = models.CharField(max_length=250)

class Tournament(models.Model):

    tournament_name = models.CharField(max_length=250)
    tournament_date = models.DateField(null=True)
    tournament_year = models.IntegerField()
