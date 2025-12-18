from rest_framework import mixins, permissions, status, viewsets
from rest_framework.response import Response

from ..models.music import Rating
from ..serializers.rating import RatingSerializer
from ..tasks import update_music_rating_stats


class RatingViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        music = serializer.validated_data.get('music')
        rating, created = Rating.objects.update_or_create(
            user=self.request.user,
            music=music,
            defaults={'score': serializer.validated_data.get('score')}
        )

        update_music_rating_stats.delay(music.id)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            {"detail": "Rating submitted successfully and is being processed."},
            status=status.HTTP_201_CREATED
        )
