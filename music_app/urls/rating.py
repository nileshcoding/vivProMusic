from django.urls import include, path
from rest_framework.routers import DefaultRouter

from ..views.rating import RatingViewSet

router = DefaultRouter()

router.register(r'rating', RatingViewSet, basename='rating')

urlpatterns = [
    path('', include(router.urls)),
]
