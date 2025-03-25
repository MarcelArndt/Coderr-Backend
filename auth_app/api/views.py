from auth_app.api.serializers import RegestrationSerializer, UserSerializer
from auth_app.models import CustomUser
from rest_framework import generics, status
from rest_framework.views import APIView 
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.authtoken.models import Token

class UserListView(generics.ListAPIView, generics.RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

class RegestrationView(APIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegestrationSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        permission_classes = [AllowAny]
        serializer = RegestrationSerializer(data= request.data)

        if serializer.is_valid():
            saved_user = serializer.save()
            token, create = Token.objects.get_or_create(user = saved_user.user)
            data = {
                "token": token.key,
                "username": saved_user.user.username,
                "email": saved_user.user.email,
                "user_id": saved_user.user.id
            }

        else:
            data = serializer.errors
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        return Response(data, status=status.HTTP_201_CREATED)
