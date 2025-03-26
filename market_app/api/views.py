from market_app.api.serializers import ProfilesSerializer
from market_app.models import Profiles
from rest_framework import generics, status
from rest_framework.views import APIView 
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, AllowAny
from .premissions import IsOwnerOrAdmin



class ProfilesFilteredListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, type, *args, **kwargs):
        if not type in ["business", "customer"]:
            return Response({"error": "type doesn't match for filtering"}, status=status.HTTP_404_NOT_FOUND)
        data = Profiles.objects.filter(type=type)
        if(data):
            serializer = ProfilesSerializer(data, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Business-User found'}, status=status.HTTP_404_NOT_FOUND)
        

class ProfilesListView(APIView):

    permission_classes = [AllowAny]
    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        user = Profiles.objects.filter(pk=pk).first()
        if user:
            serializer = ProfilesSerializer(user)
            data = serializer.data 
            data["user"] = data.pop("id")
            data["created_at"] = data.pop("date_joined")
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Nutzer nicht gefunden'}, status=status.HTTP_404_NOT_FOUND)
        
    permission_classes = [IsOwnerOrAdmin]
    def patch(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        user = Profiles.objects.filter(pk=pk).first()
        if not user:
            return Response({'error': 'Nutzer nicht gefunden'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ProfilesSerializer(user, data = request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            data = serializer.data 
            data["user"] = data.pop("id")
            data["created_at"] = data.pop("date_joined")
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            