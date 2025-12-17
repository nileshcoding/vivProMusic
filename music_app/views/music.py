from django_filters import rest_framework as filters
from rest_framework import permissions, viewsets
from rest_framework.filters import OrderingFilter

from ..models.music import Music
from ..pagination import MusicPagination
from ..serializers.music_serializers import MusicSerializer


class MusicFilter(filters.FilterSet):
    title = filters.CharFilter(lookup_expr='icontains')

    min_energy = filters.NumberFilter(field_name="energy", lookup_expr='gte')
    max_energy = filters.NumberFilter(field_name="energy", lookup_expr='lte')
    min_tempo = filters.NumberFilter(field_name="tempo", lookup_expr='gte')
    max_tempo = filters.NumberFilter(field_name="tempo", lookup_expr='lte')

    class Meta:
        model = Music
        fields = ['title', 'energy', 'danceability', 'mode']


class MusicViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Music.objects.all().order_by('-total_ratings')
    serializer_class = MusicSerializer
    pagination_class = MusicPagination

    filter_backends = (filters.DjangoFilterBackend, OrderingFilter)
    filterset_class = MusicFilter

    ordering_fields = ['average_rating', 'total_ratings', 'tempo', 'energy', 'title']

    lookup_field = 'title'
    permission_classes = [permissions.AllowAny]
