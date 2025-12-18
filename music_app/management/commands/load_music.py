import json

from django.core.management.base import BaseCommand

from music_app.models.music import Music


class Command(BaseCommand):
    help = 'Load music data from a columnar JSON file'

    def add_arguments(self, parser):
        parser.add_argument('json_file', type=str, help='Path to the JSON file')

    def handle(self, *args, **options):
        file_path = options['json_file']

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Since your JSON uses indices ("0", "1", "2"...),
            # we find out how many indices there are using the 'id' key.
            indices = data.get('id', {}).keys()
            music_objects = []

            for i in indices:
                # We pull the value for each column at index i
                music_objects.append(Music(
                    spotify_id=data['id'].get(i),
                    title=data['title'].get(i),
                    danceability=data['danceability'].get(i),
                    energy=data['energy'].get(i),
                    key=data['key'].get(i),
                    loudness=data['loudness'].get(i),
                    mode=data['mode'].get(i),
                    acousticness=data['acousticness'].get(i),
                    instrumentalness=data['instrumentalness'].get(i),
                    liveness=data['liveness'].get(i),
                    valence=data['valence'].get(i),
                    tempo=data['tempo'].get(i),
                    duration_ms=data['duration_ms'].get(i),
                    time_signature=data['time_signature'].get(i),
                    num_bars=data['num_bars'].get(i),
                    num_sections=data['num_sections'].get(i),
                    num_segments=data['num_segments'].get(i)
                ))

            # Use ignore_conflicts=True to skip songs already in the DB
            Music.objects.bulk_create(music_objects, ignore_conflicts=True)

            self.stdout.write(self.style.SUCCESS(
                f'Successfully processed {len(music_objects)} tracks from JSON.'
            ))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'An error occurred: {str(e)}'))
