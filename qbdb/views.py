from django.shortcuts import render, render_to_response
from django.template import Context, RequestContext
from django.http import HttpResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

from qbdb.models import Tossup, Bonus, Packet, Tournament
from haystack.query import SearchQuerySet

import os
import json
import re

def main(request):

    return render_to_response('main.html',
        context_instance=RequestContext(request))

@csrf_exempt
def add_tournament(request):
    """
    Takes a JSON file representing an entire tournament and
    adds it to the database
    """
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

        json_data = json.dumps([t.to_dict() for t in all_tournaments])

        return HttpResponse(json_data, content_type='application/json')


@csrf_exempt
def get_tournament(request, id):

    if request.method == 'GET':
        try:
            tournament = Tournament.objects.get(id=id)
        except Exception as ex:
            print ex
            return HttpResponse(json.dumps({'error': 'Tournament not found'}))

        packets = tournament.packet_set.all()

        #data = {'tournament': tournament.to_dict(with_packets=True)}

        return HttpResponse(tournament.to_json(with_packets=True),
                            content_type='application/json')

@csrf_exempt
def get_packet(request, id):

    if request.method == 'GET':
        try:
            packet = Packet.objects.get(id=id)
        except Exception as ex:
            print ex
            return HttpResponse(json.dumps({'error': 'Packet not found'}))

        return HttpResponse(packet.to_json(with_questions=True),
                            content_type='application/json')


@csrf_exempt
def search(request):

    if request.method == 'GET':
        print request.GET
        q = request.GET.get('q')
        models = request.GET.getlist('models')
        fields = request.GET.getlist('fields')

        results = SearchQuerySet().filter(content=q)
        results = [r for r in results if r.model_name in models]
        tu_results = []
        bs_results = []

        if 'tossup' in models:
            tu_results = [r for r in results if r.model_name == 'tossup']
        if 'bonus' in models:
            bs_results = [r for r in results if r.model_name == 'bonus']

        def none_to_str(x):
            if x is None:
                return ''
            else:
                return x

        if 'question' in fields and 'answer' not in fields:
            tu_results = [r for r in tu_results if re.search(q, r.tossup_text, re.I) is not None]
            bs_results = [r for r in bs_results if re.search(q, r.leadin_text, re.I) is not None
                                                or re.search(q, none_to_str(r.part1_text), re.I) is not None
                                                or re.search(q, none_to_str(r.part2_text), re.I) is not None
                                                or re.search(q, none_to_str(r.part3_text), re.I) is not None
                                                or re.search(q, none_to_str(r.part4_text), re.I) is not None
                                                or re.search(q, none_to_str(r.part5_text), re.I) is not None
                                                or re.search(q, none_to_str(r.part6_text), re.I) is not None]
        elif 'answer' in fields and 'question' not in fields:
            print q
            tu_results = [r for r in tu_results if re.search(q, r.answer, re.I) is not None]
            bs_results = [r for r in bs_results if re.search(q, r.leadin_text, re.I) is not None
                                                or re.search(q, none_to_str(r.part1_answer), re.I) is not None
                                                or re.search(q, none_to_str(r.part2_answer), re.I) is not None
                                                or re.search(q, none_to_str(r.part3_answer), re.I) is not None
                                                or re.search(q, none_to_str(r.part4_answer), re.I) is not None
                                                or re.search(q, none_to_str(r.part5_answer), re.I) is not None
                                                or re.search(q, none_to_str(r.part6_answer), re.I) is not None]
        elif 'answer' in fields and 'question' in fields:
            tu_results = [r for r in tu_results if re.search(q, r.tossup_text, re.I) is not None
                                                or re.search(q, r.answer, re.I) is not None]

            bs_results = [r for r in bs_results if re.search(q, none_to_str(r.leadin_text), re.I) is not None
                                                or re.search(q, none_to_str(r.part1_text), re.I) is not None
                                                or re.search(q, none_to_str(r.part2_text), re.I) is not None
                                                or re.search(q, none_to_str(r.part3_text), re.I) is not None
                                                or re.search(q, none_to_str(r.part4_text), re.I) is not None
                                                or re.search(q, none_to_str(r.part5_text), re.I) is not None
                                                or re.search(q, none_to_str(r.part6_text), re.I) is not None
                                                or re.search(q, none_to_str(r.part1_answer), re.I) is not None
                                                or re.search(q, none_to_str(r.part2_answer), re.I) is not None
                                                or re.search(q, none_to_str(r.part3_answer), re.I) is not None
                                                or re.search(q, none_to_str(r.part4_answer), re.I) is not None
                                                or re.search(q, none_to_str(r.part5_answer), re.I) is not None
                                                or re.search(q, none_to_str(r.part6_answer), re.I) is not None]

        print tu_results

        tossup_ids = [int(r.id.split('.')[-1]) for r in tu_results]
        bonus_ids = [int(r.id.split('.')[-1]) for r in bs_results]

        tossups = Tossup.objects.filter(id__in=tossup_ids)
        bonuses = Bonus.objects.filter(id__in=bonus_ids)

        print tossups

        return HttpResponse(json.dumps({'tossups': [t.to_dict() for t in tossups],
                                        'bonuses': [b.to_dict() for b in bonuses]}),
                            content_type='application/json')

def faq(request):

    if request.method == 'GET':

        return render_to_response('faq.html',
                                  context_instance=RequestContext(request))
