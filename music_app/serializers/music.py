from rest_framework import serializers

from ..models.music import Music


class MusicSerializer(serializers.ModelSerializer):
    # These fields are now real database columns updated by Celery
    class Meta:
        model = Music
        fields = [
            'id',
            'spotify_id',
            'title',
            'average_rating',  # Pre-calculated by Celery
            'total_ratings',   # Pre-calculated by Celery
            'danceability',
            'energy',
            'key',
            'loudness',
            'mode',
            'acousticness',
            'instrumentalness',
            'liveness',
            'valence',
            'tempo',
            'duration_ms',
            'time_signature',
            'num_bars',
            'num_sections',
            'num_segments'
        ]
        read_only_fields = [
            'spotify_id',
            'average_rating',
            'total_ratings'
        ]
