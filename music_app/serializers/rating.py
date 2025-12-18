from rest_framework import serializers

from ..models.music import Rating


class RatingSerializer(serializers.ModelSerializer):
    # 'user' is read-only because we assign it automatically in the view
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Rating
        fields = ['id', 'user', 'music', 'score']

    def validate_score(self, value):
        if not (1 <= value <= 5):
            raise serializers.ValidationError("Rating score must be between 1 and 5.")
        return value

    def validate(self, data):
        return data
