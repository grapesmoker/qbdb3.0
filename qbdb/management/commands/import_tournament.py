from django.core.management.base import BaseCommand, CommandError
from qbdb.views import add_tournament
from qbdb.utils import put_tournament_into_db

import json

class Command(BaseCommand):

    help = 'Imports specified tournament JSON file into the database.'

    def add_arguments(self, parser):
        parser.add_argument('tournament_json_file', nargs='?')

    def handle(self, *args, **options):

        if 'tournament_json_file' in options:
            tour_file = options['tournament_json_file']
            tour_data = json.load(open(tour_file, 'r'))
            put_tournament_into_db(tour_data)
            print 'imported', tour_file

        else:
            raise CommandError('Must supply file to import.')
