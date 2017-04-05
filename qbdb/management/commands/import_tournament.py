from django.core.management.base import BaseCommand, CommandError
from qbdb.views import add_tournament
from qbdb.utils import put_tournament_into_db

import json

class Command(BaseCommand):

    help = 'Imports specified tournament JSON file into the database.'

    def add_arguments(self, parser):
        parser.add_argument('tournament_json_files', nargs='*')

    def handle(self, *args, **options):

        if 'tournament_json_files' in options:
            for tour_file in options['tournament_json_files']:
                tour_data = json.load(open(tour_file, 'r'))
                put_tournament_into_db(tour_data)
                print 'imported', tour_file

        else:
            raise CommandError('Must supply one or more files to import.')
