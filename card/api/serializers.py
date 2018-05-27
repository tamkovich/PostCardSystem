from rest_framework import serializers

from card.models import UserCard


class UserCardSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = UserCard
        fields = [
            'url',
            'pk',
            'city',
            'visited_date',
            'transport',
            'value',
        ]
        read_only_fields = ['pk']

    def get_url(self, obj):
        request = self.context.get("request")
        return obj.get_api_url(request=request)

    # def validate_pk(self, value):
    #     qs = UserCard.objects.filter(pk=value)
    #     if qs.exists():
    #         raise serializers.ValidationError("The id must be unique")
