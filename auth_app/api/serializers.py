from rest_framework import serializers
from coderr_market_app.models import Profiles, BUSINESSTYPE_CHOICES
from django.contrib.auth.models import User


class RegestrationSerializer(serializers.ModelSerializer):
    repeated_password = serializers.CharField(write_only = True)
    password = serializers.CharField(write_only = True)
    email = serializers.EmailField(write_only=True)
    username = serializers.CharField(write_only = True)
    type = serializers.ChoiceField(choices=BUSINESSTYPE_CHOICES, write_only = True)

    class Meta():
        model = Profiles
        fields = ["username", "email", "type", "password", "repeated_password"]
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate(self, data):
        password = data.get("password")
        repeatingPassword = data.get("repeated_password")
        email = data.get("email")
        username = data.get("username")

        if User.objects.filter(username = username).exists():
            raise serializers.ValidationError({'username':"Username already exists."})
        if not repeatingPassword == password:
            raise serializers.ValidationError({'password':"passwords doesn't match"})
        if not email:
            raise serializers.ValidationError({'email':"Email is required."})
        if User.objects.filter(email = email).exists():
            raise serializers.ValidationError({'email':"Email already exists."}) 
        
        return data

    def create(self, validated_data) :
        password = self.validated_data.get('password')
        type = self.validated_data.get('type')
        email = self.validated_data.get("email")
        username = self.validated_data.get('username')
        user = User.objects.create_user(username = username, email = email, password = password)
        user_profiles = Profiles.objects.create(user = user, type = type)
        return user_profiles

class LoginSerializer(serializers.Serializer):
        username = serializers.CharField(write_only=True)
        password = serializers.CharField(write_only=True)

        def validate(self, data):
            username = data.get("username")
            password = data.get("password")
            user = User.objects.filter(username=username).first()
            if not user:
                raise serializers.ValidationError({'username':"wrong username"})

            if not user.check_password(password):
                 raise serializers.ValidationError({'password':"wrong password"})
            try:
                user_profile = user.inner_user
            except:
                raise serializers.ValidationError({'user':"No User found"})

            return {"user_profile" : user_profile}

               
            
        
