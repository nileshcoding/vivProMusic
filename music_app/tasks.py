from celery import shared_task
from django.db.models import Avg, Count

from .models.music import Music


@shared_task
def update_music_rating_stats(music_id):
    music = Music.objects.get(id=music_id)
    stats = music.ratings.aggregate(avg_score=Avg("score"), count=Count("id"))

    music.average_rating = stats["avg_score"] or 0.0
    music.total_ratings = stats["count"] or 0
    music.save()
