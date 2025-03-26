from rest_framework import serializers
from django.contrib.auth.models import User
from market_app.models import Profiles

class ProfilesSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username")
    email = serializers.EmailField(source="user.email")
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")
    date_joined = serializers.DateTimeField(source="user.date_joined", format="%Y-%m-%dT%H:%M:%S")

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})
        user = instance.user

        for key, value in user_data.items():
            setattr(user, key, value)
        user.save()

        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()

        return instance

    class Meta():
        model = Profiles
        exclude = ["user"]
