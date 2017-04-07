from django.shortcuts import render, render_to_response
from django.template import Context, RequestContext
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect, JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.contrib.auth import login, logout, authenticate
from django.core.validators import EmailValidator, ValidationError
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core import serializers

from qbdb.models import *
from qbdb.utils import put_tournament_into_db
from haystack.query import SearchQuerySet

from django.conf import settings

import os
import json
import re
import random
import requests

# This is sort of stupid, but to select a random question from the db, you need to know the IDs,
# unless there are no deletions in the table, which there are not. So when we load up, just fetch
# all the tossup and bonus IDs into a list that we can then check as needed. This means that if you
# load new data you have to restart the application, but who cares, we need to do that to index
# anyway, so it's no big deal.

tossup_ids = [tossup.id for tossup in Tossup.objects.all()]
bonus_ids = [bonus.id for bonus in Bonus.objects.all()]


def register(request):

    if request.method == 'GET':
        if request.user.is_authenticated():
            user = request.user
        else:
            user = None

        return render(request, 'register.html',
                {'user': user})

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

        if errors:
            user_data = {'username': username,
                         'email': email,
                         'first_name': first_name,
                         'last_name': last_name,
                         'affiliation': affiliation}

            return render(request, 'register.html', {'errors': errors, 'user_data': user_data})

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
                    return render(request, 'login.html', {'errors': errors})

            else:
                errors.append('Invalid login.')
                return render(request, 'login.html', {'errors': errors})
        else:
            errors.append('What are you doing? You are already logged in!')
            return render(request, 'login.html', {'errors': errors})

    elif request.method == 'GET':
        return render(request, 'login.html')


def main(request):

    if request.method == 'GET':

        if request.user.is_authenticated():
            user = request.user
        else:
            user = None

        return render(request, 'main.html', {'user': user})

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

    try:
        put_tournament_into_db(tour_data)
    except Exception as ex:
        print ex
        return HttpResponse(json.dumps({'error': str(ex)}),
                            content_type='application/json')
    return HttpResponse(json.dumps({'result': 'success'}),
                        content_type='application/json')


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
def get_random_question(request):

    if request.method == 'GET':

        question_type = request.GET['question_type']
        if question_type == 'either':
            coin = random.random()
            if coin > 0.5:
                question_type = 'tossup'
            else:
                question_type = 'bonus'

        if question_type == 'tossup':
            random_id = random.choice(tossup_ids)
            result = Tossup.objects.get(id=random_id)
        elif question_type == 'bonus':
            random_id = random.choice(bonus_ids)
            result = Bonus.objects.get(id=random_id)

        question_json = json.loads(serializers.serialize('json', [result]))[0]
        question_json['fields']['tournament_name'] = \
            Tournament.objects.get(id=question_json['fields']['tournament']).tournament_name
        question_json['fields']['author'] = Packet.objects.get(id=question_json['fields']['packet']).author

        if question_type == 'bonus':
            bonus_parts = BonusPart.objects.filter(bonus__id=question_json['pk'])
            bpart_json = json.loads(serializers.serialize('json', bonus_parts))
            for bonus_part in bpart_json:
                for key, value in bonus_part['fields'].items():
                    bonus_part[key] = value
                del bonus_part['fields']
            question_json['fields']['bonus_parts'] = bpart_json

        for key, value in question_json['fields'].items():
            question_json[key] = value
        del question_json['fields']

        return HttpResponse(json.dumps(question_json),
                            content_type='application/json')

@csrf_exempt
def search(request):

    if request.method == 'GET':
        q = request.GET.get('q')
        models = request.GET.getlist('models')
        fields = request.GET.getlist('fields')

        tu_results = []
        bs_results = []
        bp_results = []

        if 'question' in fields and 'answer' not in fields:
            if 'tossup' in models:
                tu_results = SearchQuerySet().filter(tossup_text=q).models(Tossup)

            if 'bonus' in models:
                bs_results = SearchQuerySet().filter(leadin_text=q).models(Bonus)
                bp_results = SearchQuerySet().filter(part_text=q).models(BonusPart)

        elif 'answer' in fields and 'question' not in fields:
            if 'tossup' in models:
                print 'getting tossups for {} with only questions'.format(q)
                tu_results = SearchQuerySet().filter(tossup_answer=q).models(Tossup)

            if 'bonus' in models:
                bp_results = SearchQuerySet().filter(bonus_answer=q).models(BonusPart)

        elif 'answer' in fields and 'question' in fields:
            if 'tossup' in models:
                print 'getting tossups for {} with questions and answers'.format(q)
                tu_results = SearchQuerySet().filter(content=q).models(Tossup)

            if 'bonus' in models:
                print 'getting bonuses for {} with questions and answers'.format(q)
                bs_results = SearchQuerySet().filter(content=q).models(Bonus)
                bp_results = SearchQuerySet().filter(content=q).models(BonusPart)

        tossups_json = json.loads(serializers.serialize('json', [r.object for r in tu_results]))
        for tossup in tossups_json:
            tossup['fields']['tournament_name'] = \
                Tournament.objects.get(id=tossup['fields']['tournament']).tournament_name
            tossup['fields']['author'] = Packet.objects.get(id=tossup['fields']['packet']).author
            tossup['id'] = tossup.pop('pk')
            tossup['fields']['tour_id'] = tossup['fields'].pop('tournament')
            tossup['fields']['pack_id'] = tossup['fields'].pop('packet')
            for key, value in tossup['fields'].items():
                tossup[key] = value
            del tossup['fields']

        # print q, tossups_json

        bonuses = [r.object for r in bs_results]

        for r in bp_results:
            if r.object.bonus not in bonuses:
                bonuses.append(r.object.bonus)

        bonuses_json = json.loads(serializers.serialize('json', bonuses))
        for bonus in bonuses_json:
            bonus_parts = BonusPart.objects.filter(bonus__id=bonus['pk'])
            bpart_json = json.loads(serializers.serialize('json', bonus_parts))
            for bonus_part in bpart_json:
                for key, value in bonus_part['fields'].items():
                    bonus_part[key] = value
                del bonus_part['fields']
            bonus['fields']['bonus_parts'] = bpart_json
            bonus['fields']['tournament_name'] = \
                Tournament.objects.get(id=bonus['fields']['tournament']).tournament_name
            bonus['fields']['author'] = Packet.objects.get(id=bonus['fields']['packet']).author
            bonus['id'] = bonus.pop('pk')
            bonus['fields']['tour_id'] = bonus['fields'].pop('tournament')
            bonus['fields']['pack_id'] = bonus['fields'].pop('packet')
            for key, value in bonus['fields'].items():
                bonus[key] = value
            del bonus['fields']

        return HttpResponse(json.dumps({'tossups': tossups_json,
                                        'bonuses': bonuses_json}),
                            content_type='application/json')

def faq(request):

    if request.method == 'GET':

        if request.user.is_authenticated():
            user = request.user
        else:
            user = None

        return render_to_response(request, 'faq.html', {'user': user})

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
