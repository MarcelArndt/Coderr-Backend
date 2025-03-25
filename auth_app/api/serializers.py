from rest_framework import serializers
from auth_app.models import CustomUser, BUSINESSTYPE_CHOICES
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source="user.email", read_only = True)
    name = serializers.CharField(source="user.username", read_only = True)

    class Meta():
        model = CustomUser
        exclude = []
        extra_kwargs = {
            'user': {'required': False}
        }


class RegestrationSerializer(serializers.ModelSerializer):
    repeated_password = serializers.CharField(write_only = True)
    password = serializers.CharField(write_only = True)
    email = serializers.EmailField(write_only=True)
    username = serializers.CharField(write_only = True)
    type = serializers.ChoiceField(choices=BUSINESSTYPE_CHOICES, write_only = True)

    class Meta():
        model = CustomUser
        fields = ["username", "password", "repeated_password", "email", "type"]
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate(self, data):
        password = data.get("password")
        repeatingPassword = data.get("repeated_password")
        email = data.get("email")

        if not repeatingPassword == password:
            raise serializers.ValidationError("Passwörter stimmen nicht überein")
 
        if not email:
            raise serializers.ValidationError({"email": "Email is required"})
        
        if User.objects.filter(email = email).exists():
            raise serializers.ValidationError({"email": "Email already exists"}) 
        
        return data

    def create(self, validated_data) :
        password = self.validated_data.get('password')
        email = self.validated_data.get('email')
        type = self.validated_data.get('type')
        username = self.validated_data.get('username')

        user = User.objects.create_user(username = username, email = 'lea@web.de', password = password)
        custom_user = CustomUser.objects.create(user = user, type = type)
 
        return custom_user
