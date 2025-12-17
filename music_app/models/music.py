from django.contrib.auth.models import User
from django.contrib.postgres.indexes import GistIndex
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Music(models.Model):
    spotify_id = models.CharField(max_length=100, unique=True, db_index=True)
    title = models.CharField(max_length=255, db_index=True)

    danceability = models.FloatField()
    energy = models.FloatField()
    key = models.IntegerField()
    loudness = models.FloatField()
    mode = models.IntegerField()
    acousticness = models.FloatField()
    instrumentalness = models.FloatField()
    liveness = models.FloatField()
    valence = models.FloatField()
    tempo = models.FloatField()

    duration_ms = models.IntegerField()
    time_signature = models.IntegerField()
    num_bars = models.IntegerField()
    num_sections = models.IntegerField()
    num_segments = models.IntegerField()

    average_rating = models.FloatField(default=0.0)
    total_ratings = models.IntegerField(default=0)

    class Meta:
        indexes = [
            models.Index(fields=["title"], name="idx_music_title_search"),
            GistIndex(
                fields=["title"],
                name="idx_music_title_trgm",
                opclasses=["gist_trgm_ops"],
            ),
        ]

    def __str__(self):
        return self.title


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    music = models.ForeignKey(Music, related_name="ratings", on_delete=models.CASCADE)
    score = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

    class Meta:
        app_label = "music_app"
        unique_together = ("user", "music")
