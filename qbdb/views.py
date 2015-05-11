from django.shortcuts import render, render_to_response
from django.template import Context, RequestContext
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.contrib.auth import login, logout, authenticate
from django.core.validators import EmailValidator, ValidationError
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from qbdb.models import *
from haystack.query import SearchQuerySet

from django.conf import settings

import os
import json
import re

def register(request):

    if request.method == 'GET':
        if request.user.is_authenticated():
            user = request.user
        else:
            user = None

        return render_to_response('register.html',
                {'user': user},
                context_instance=RequestContext(request))

    elif request.method == 'POST':

        errors = []

        username = request.POST['username']
        email = request.POST['email']
        first_name = request.POST['first-name']
        last_name = request.POST['last-name']
        affiliation = request.POST['affiliation']
        pass1 = request.POST['password1']
        pass2 = request.POST['password2']

        other_users = User.objects.filter(username=username)

        if other_users.exists():
            errors.append('A user with that username already exists.')

        if pass1 == '' or pass2 == '':
            errors.append('Password cannot be empty.')
        elif pass1 != pass2:
            errors.append('The two passwords you entered do not match.')

        if username is None or username.strip() == '':
            errors.append('Must enter a username.')

        emv = EmailValidator()
        try:
            res = emv(email)
        except ValidationError as ex:
            errors.append(ex.message)

        if first_name is None or first_name.strip() == '':
            errors.append('Enter a first name.')
        if last_name is None or last_name.strip() == '':
            errors.append('Enter a last name.')

        if errors != []:
            user_data = {'username': username,
                         'email': email,
                         'first_name': first_name,
                         'last_name': last_name,
                         'affiliation': affiliation}

            return render_to_response('register.html',
                                     {'errors': errors,
                                      'user_data': user_data},
                                      context_instance=RequestContext(request))

        else:
            user = User.objects.create_user(username, email, pass1)
            user.last_name = last_name
            user.first_name = first_name
            user.save()

            qbdb_user = QBDBUser()
            qbdb_user.user = user
            qbdb_user.affiliation = affiliation
            qbdb_user.save()

            user = authenticate(username=username, password=pass1)
            login(request, user)

            return HttpResponseRedirect('/')

        return render_to_response('register.html',
                context_instance=RequestContext(request))


def do_logout(request):

    if request.method == 'GET':
        if request.user.is_authenticated():
            logout(request)

        return HttpResponseRedirect('/')


def do_login(request):

    errors = []

    if request.method == 'POST':
        if not request.user.is_authenticated():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect('/')
                else:
                    errors.append('Your account has been disabled.')
                    return render_to_response('login.html',
                            {'errors': errors},
                            context_instance=RequestContext(request))
            else:
                errors.append('Invalid login.')
                return render_to_response('login.html',
                        {'errors': errors},
                        context_instance=RequestContext(request))
        else:
            errors.append('What are you doing? You are already logged in!')
            return render_to_response('login.html',
                    {'errors': errors},
                    context_instance=RequestContext(request))

    elif request.method == 'GET':
        return render_to_response('login.html',
                context_instance=RequestContext(request))

def main(request):

    if request.method == 'GET':

        if request.user.is_authenticated():
            user = request.user
        else:
            user = None

        return render_to_response('main.html',
            {'user': user},
            context_instance=RequestContext(request))

@csrf_exempt
def add_tournament(request):
    """
    Takes a JSON file representing an entire tournament and
    adds it to the database
    """

    # if we're in production, no adding allowed
    if settings.PRODUCTION:
        return HttpResponseForbidden()

    tour_data = json.loads(request.body)
    tour_year = tour_data['year']
    tour_name = tour_data['tournament']

    # delete everything pertaining to this tournament
    tour = Tournament.objects.filter(tournament_year=tour_year, tournament_name=tour_name)

    if tour.exists():
        for packet in tour[0].packet_set.all():
            for tossup in packet.tossup_set.all():
                tossup.delete()
            for bonus in packet.bonus_set.all():
                bonus.delete()

            packet.delete()
        new_tour = tour[0]
    else:
        new_tour = Tournament()

    new_tour.tournament_year = tour_year
    new_tour.tournament_name = tour_name
    new_tour.save()

    packets = tour_data['packets']
    for packet in packets:
        new_packet = Packet()
        new_packet.tournament = new_tour
        new_packet.author = packet['author']
        new_packet.save()

        for tossup in packet['tossups']:
            new_tossup = Tossup()
            new_tossup.tossup_text = tossup['question']
            new_tossup.answer = tossup['answer']
            new_tossup.tossup_text_sanitized = tossup['question_sanitized']
            new_tossup.answer_sanitized = tossup['answer_sanitized']
            new_tossup.number = int(tossup['number'])
            new_tossup.packet = new_packet
            new_tossup.tournament = new_tour
            new_tossup.save()

        for bonus in packet['bonuses']:
            new_bonus = Bonus()
            new_bonus.packet = new_packet
            new_bonus.tournament = new_tour
            new_bonus.leadin = bonus['leadin']
            new_bonus.leadin_sanitized = bonus['leadin_sanitized']
            new_bonus.number = int(bonus['number'])
            bonus_data = zip(bonus['parts'], bonus['answers'], bonus['values'], bonus['parts_sanitized'], bonus['answers_sanitized'])
            for i, bpart in enumerate(bonus_data, start=1):
                fields = ['text', 'answer', 'value', 'text_sanitized', 'answer_sanitized']
                fields_and_values = zip(fields, bpart)
                for f in fields_and_values:
                    bonus_field = 'part{0}_{1}'.format(i, f[0])
                    setattr(new_bonus, bonus_field, f[1])

            new_bonus.save()

    #return HttpResponse(json.dumps({}), content_type='application/json')
    return HttpResponse('ok')


@csrf_exempt
def tournaments(request):

    if request.method == 'GET':
        all_tournaments = Tournament.objects.all()

        if request.user.is_authenticated():
            qbdb_user = request.user.qbdbuser
        else:
            qbdb_user = None

        json_data = json.dumps([t.to_dict(user=qbdb_user) for t in all_tournaments])

        return HttpResponse(json_data, content_type='application/json')


@csrf_exempt
def get_tournament(request, id):

    if request.method == 'GET':

        if request.user.is_authenticated():
            qbdb_user = request.user.qbdbuser
        else:
            qbdb_user = None


        try:
            tournament = Tournament.objects.get(id=id)
        except Exception as ex:
            print ex
            return HttpResponse(json.dumps({'error': 'Tournament not found'}))

        packets = tournament.packet_set.all()

        return HttpResponse(tournament.to_json(with_packets=True, user=qbdb_user),
                            content_type='application/json')

@csrf_exempt
def get_packet(request, id):

    if request.method == 'GET':

        if request.user.is_authenticated():
            qbdb_user = request.user.qbdbuser
        else:
            qbdb_user = None

        try:
            packet = Packet.objects.get(id=id)
        except Exception as ex:
            print ex
            return HttpResponse(json.dumps({'error': 'Packet not found'}))

        return HttpResponse(packet.to_json(with_questions=True, user=qbdb_user),
                            content_type='application/json')


@csrf_exempt
def search(request):

    if request.method == 'GET':
        q = request.GET.get('q')
        models = request.GET.getlist('models')
        fields = request.GET.getlist('fields')

        if 'question' in fields and 'answer' not in fields:
            if 'tossup' in models:
                tu_results = SearchQuerySet().filter(Q(tossup_text=q)).models(Tossup)
            else:
                tu_results = []

            if 'bonus' in models:
                bs_results = SearchQuerySet().filter(Q(leadin_text=q) |
                                                     Q(part1_text=q)  |
                                                     Q(part2_text=q)  |
                                                     Q(part3_text=q)  |
                                                     Q(part4_text=q)  |
                                                     Q(part5_text=q)  |
                                                     Q(part6_text=q)).models(Bonus)
            else:
                bs_results = []

        elif 'answer' in fields and 'question' not in fields:
            if 'tossup' in models:
                tu_results = SearchQuerySet().filter(Q(answer=q)).models(Tossup)
            else:
                tu_results = []

            if 'bonus' in models:
                bs_results = SearchQuerySet().filter(Q(part1_answer=q)  |
                                                     Q(part2_answer=q)  |
                                                     Q(part3_answer=q)  |
                                                     Q(part4_answer=q)  |
                                                     Q(part5_answer=q)  |
                                                     Q(part6_answer=q)).models(Bonus)
            else:
                bs_results = []

        elif 'answer' in fields and 'question' in fields:
            if 'tossup' in models:
                tu_results = SearchQuerySet().filter(content=q).models(Tossup)
            else:
                tu_results = []

            if 'bonus' in models:
                bs_results = SearchQuerySet().filter(content=q).models(Bonus)
            else:
                bs_results = []

        tossups = [r.object for r in tu_results]
        bonuses = [r.object for r in bs_results]

        return HttpResponse(json.dumps({'tossups': [t.to_dict() for t in tossups],
                                        'bonuses': [b.to_dict() for b in bonuses]}),
                            content_type='application/json')

def faq(request):

    if request.method == 'GET':

        if request.user.is_authenticated():
            user = request.user
        else:
            user = None

        return render_to_response('faq.html',
                                 {'user': user},
                                  context_instance=RequestContext(request))

@login_required
def vote(request):

    if request.method == 'POST':
        diff_rank = None
        qual_rank = None

        if 'diff' in request.POST:
            diff_rank = request.POST['diff']
        if 'qual' in request.POST:
            qual_rank = request.POST['qual']

        if 'tournament_id' in request.POST:
            model = Tournament
            obj_id = request.POST['tournament_id']
            vote_model = TournamentVote
            vote_field = 'tournament'
            vote_set = 'tournamentvote_set'

        elif 'packet_id' in request.POST:
            model = Packet
            obj_id = request.POST['packet_id']
            vote_model = PacketVote
            vote_field = 'packet'
            vote_set = 'packetvote_set'

        elif 'tossup_id' in request.POST:
            model = Tossup
            obj_id = request.POST['tossup_id']
            vote_model = TossupVote
            vote_field = 'tossup'
            vote_set = 'tossupvote_set'

        elif 'bonus_id' in request.POST:
            model = Bonus
            obj_id = request.POST['bonus_id']
            vote_model = BonusVote
            vote_field = 'bonus'
            vote_set = 'bonusvote_set'

        try:
            user = request.user.qbdbuser
            model_obj = model.objects.get(id=obj_id)

            # only one vote allowed per user
            new_vote = vote_model.objects.filter(**{'user': user, vote_field: model_obj})

            if new_vote.exists():
                new_vote = new_vote.first()
            else:
                new_vote = vote_model(**{'user': user, vote_field: model_obj})

            if diff_rank:
                diff = int(diff_rank)
                new_vote.difficulty = diff
            if qual_rank:
                qual = int(qual_rank)
                new_vote.quality = qual

            new_vote.save()

            if 'diff' in request.POST:
                total_diffs = [vote.difficulty for vote in getattr(model_obj, vote_set).all() if vote.difficulty > 0]
                if len(total_diffs) > 0:
                    model_obj.difficulty = float(sum(total_diffs)) / float(len(total_diffs))
                else:
                    model_obj.difficulty = 0
            if 'qual' in request.POST:
                total_quals = [vote.quality for vote in getattr(model_obj, vote_set).all() if vote.quality > 0]
                if len(total_quals) > 0:
                    model_obj.quality = float(sum(total_quals)) / float(len(total_quals))
                else:
                    model_obj.quality = 0

            model_obj.save()

            return HttpResponse(json.dumps({'result': 'success',
                                            'id': int(obj_id),
                                            'diff': model_obj.difficulty,
                                            'qual': model_obj.quality}),
                    content_type='application/json')

        except Exception as ex:

            print ex
