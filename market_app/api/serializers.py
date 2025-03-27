from rest_framework import serializers
from django.contrib.auth.models import User
from market_app.models import Profiles, Offers, OffersDetails



### Offers ### _________________________________________________________________________

class OffersDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OffersDetails
        exclude = ['offer']


class OffersSerializer(serializers.ModelSerializer):
    details = OffersDetailSerializer(many=True, read_only=True)
    username = serializers.CharField(source='user.user.username', read_only=True)
    class Meta:
        model = Offers
        exclude = []
        extra_kwargs = {
            'user': {'read_only': True}
        }


class CreateOffersSerializer(serializers.ModelSerializer):
    details = OffersDetailSerializer(many=True)

    class Meta:
        model = Offers
        fields = '__all__'
        read_only_fields = ['user']

    def create(self, validated_data):  
        
        if "details" not in validated_data:
            raise serializers.ValidationError({"details": "Dieses Feld ist erforderlich."})
        details_list = validated_data.pop('details', [])
        
        print(f"current User {validated_data.get('user')}")
        user = self.context.get('request').user
        if not user.is_authenticated:
            raise serializers.ValidationError("You must be logged in to create an offer.")
        else: 
            profile = Profiles.objects.get(user=user)

        validated_data['user'] = profile

        new_offer = Offers.objects.create(**validated_data)  

        for each_detail in details_list:
            each_detail["offer"] = new_offer
            OffersDetails.objects.create(**each_detail)

        return new_offer
    



### Profiles ### _______________________________________________________________________

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
