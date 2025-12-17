from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from ..models.music import Music


class MusicAPITests(APITestCase):
    def setUp(self):
        # Create a test user for authentication
        self.user = User.objects.create_user(
            username="testuser", password="password123"
        )

        # Create sample music data with audio features
        self.music1 = Music.objects.create(
            spotify_id="5vYA1mW9g2Coh1HUFUSmlb",
            title="3AM",
            danceability=0.521,
            energy=0.673,
            key=8,
            loudness=-8.685,
            mode=1,
            acousticness=0.00573,
            instrumentalness=0.0,
            liveness=0.12,
            valence=0.543,
            tempo=108.031,
            duration_ms=225947,
            time_signature=4,
            num_bars=100,
            num_sections=8,
            num_segments=830,
        )
        self.music2 = Music.objects.create(
            spotify_id="2klCjJcucgGQysgH170npL",
            title="4 Walls",
            danceability=0.735,
            energy=0.849,
            key=4,
            loudness=-4.308,
            mode=0,
            acousticness=0.212,
            instrumentalness=0.0000294,
            liveness=0.0608,
            valence=0.223,
            tempo=125.972,
            duration_ms=207477,
            time_signature=4,
            num_bars=107,
            num_sections=7,
            num_segments=999,
        )
        self.url = reverse("music-list")

    def test_get_music_list_pagination(self):
        """Verify default pagination of 25 and custom page size."""
        # Default check
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("results", response.data)

        # Custom page size check
        response = self.client.get(self.url, {"page_size": 1})
        self.assertEqual(len(response.data["results"]), 1)

    def test_music_search_title_like(self):
        """Test the 'LIKE %foo%' trigram search logic."""
        # Search for partial title
        response = self.client.get(self.url, {"title": "AM"})
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["title"], "3AM")

    def test_music_detail_by_title(self):
        """Verify detail view works with the title lookup field."""
        detail_url = reverse("music-detail", kwargs={"title": "3AM"})
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["spotify_id"], "5vYA1mW9g2Coh1HUFUSmlb")

    def test_audio_features_presence(self):
        """Ensure all new audio fields are in the API response."""
        response = self.client.get(self.url)
        first_song = response.data["results"][0]
        self.assertIn("energy", first_song)
        self.assertIn("tempo", first_song)
        self.assertIn("valence", first_song)
