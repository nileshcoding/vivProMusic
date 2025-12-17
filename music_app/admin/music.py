from django.contrib import admin

from ..models.music import Music, Rating


@admin.register(Music)
class MusicAdmin(admin.ModelAdmin):
    list_display = ("title", "spotify_id", "tempo", "danceability", "energy", "valence")

    search_fields = ("title", "spotify_id")

    list_filter = ("key", "mode", "time_signature")

    fieldsets = (
        ("Core Identification", {"fields": ("title", "spotify_id")}),
        (
            "Audio Features",
            {
                "fields": (
                    "danceability",
                    "energy",
                    "key",
                    "loudness",
                    "mode",
                    "acousticness",
                    "instrumentalness",
                    "liveness",
                    "valence",
                    "tempo",
                )
            },
        ),
        (
            "Technical Metadata",
            {
                "classes": ("collapse",),
                "fields": (
                    "duration_ms",
                    "time_signature",
                    "num_bars",
                    "num_sections",
                    "num_segments",
                ),
            },
        ),
    )

    readonly_fields = ("spotify_id",)


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ("user", "music", "score")
    list_filter = ("score",)
    raw_id_fields = ("music", "user")
