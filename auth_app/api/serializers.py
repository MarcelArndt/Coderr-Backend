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
            raise serializers.ValidationError("Username already exists.")
        if not repeatingPassword == password:
            raise serializers.ValidationError("passwords doesn't match")
        if not email:
            raise serializers.ValidationError("Email is required.")
        if User.objects.filter(email = email).exists():
            raise serializers.ValidationError("Email already exists.") 
        
        return data

    def create(self, validated_data) :
        password = self.validated_data.get('password')
        type = self.validated_data.get('type')
        email = self.validated_data.get("email")
        username = self.validated_data.get('username')
        user = User.objects.create_user(username = username, email = email, password = password)
        custom_user = CustomUser.objects.create(user = user, type = type)
        return custom_user

class LoginSerializer(serializers.Serializer):
        username = serializers.CharField(write_only=True)
        password = serializers.CharField(write_only=True)

        def validate(self, data):
            username = data.get("username")
            password = data.get("password")
            user = User.objects.filter(username=username).first()
            if not user:
                raise serializers.ValidationError("wrong username")

            if not user.check_password(password):
                 raise serializers.ValidationError("wrong password")
            
            try:
                custom_user = user.above_user
            except:
                raise serializers.ValidationError("No User found")

            return {"custom_user" : custom_user}

               
            
        
