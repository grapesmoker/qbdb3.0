from tastypie.resources import ModelResource
from tastypie import fields
from tastypie.constants import *
from qbdb.models import *


class TournamentResource(ModelResource):

    #packets = fields.OneToManyField('qbdb.api.PacketResource', 'packet_set', full=True)
    packets = fields.ListField(attribute='packets');
    name = fields.CharField(attribute='tournament_name')
    id = fields.IntegerField(attribute='id')

    class Meta:
        queryset = Tournament.objects.all()
        resource_name = 'tournament'
        limit = 0


class PacketResource(ModelResource):

    tournament = fields.ToOneField('qbdb.api.TournamentResource', 'tournament', readonly=True)
    tournament_name = fields.CharField(attribute='tournament_name')
    tour_id = fields.IntegerField(attribute='tour_id')
    tossups = fields.ToManyField('qbdb.api.TossupResource', 'tossup_set', full=True, readonly=True)
    bonuses = fields.ToManyField('qbdb.api.BonusResource', 'bonus_set', full=True, readonly=True)

    class Meta:
        queryset = Packet.objects.all()
        resource_name = 'packet'
        filtering = {
            'tournament': ALL_WITH_RELATIONS
        }
        limit = 50


class TossupResource(ModelResource):

    packet = fields.ToOneField('qbdb.api.PacketResource', 'packet', readonly=True)
    tournament = fields.ToOneField('qbdb.api.TournamentResource', 'tournament', readonly=True)

    tournament_name = fields.CharField(attribute='tournament_name')
    tour_id = fields.IntegerField(attribute='tour_id')
    author = fields.CharField(attribute='author')
    pack_id = fields.IntegerField(attribute='pack_id')

    class Meta:
        queryset = Tossup.objects.all()
        resource_name = 'tossup'


class BonusResource(ModelResource):

    packet = fields.ToOneField('qbdb.api.PacketResource', 'packet', readonly=True)
    tournament = fields.ToOneField('qbdb.api.TournamentResource', 'tournament', readonly=True)

    tournament_name = fields.CharField(attribute='tournament_name')
    tour_id = fields.IntegerField(attribute='tour_id')
    author = fields.CharField(attribute='author')
    pack_id = fields.IntegerField(attribute='pack_id')

    bonus_parts = fields.ToManyField('qbdb.api.BonusPartResource', 'bonuspart_set', full=True, readonly=True)

    class Meta:
        queryset = Bonus.objects.all()
        resource_name = 'bonus'


class BonusPartResource(ModelResource):

    bonus = fields.ToOneField('qbdb.api.BonusResource', 'bonus', readonly=True)

    class Meta:
        queryset = BonusPart.objects.all()
        resource_name = 'bonus_part'