from market_app.api.serializers import ProfilesSerializer, OffersSerializer, OffersDetailSerializer, CreateOffersSerializer, ReviewsSerializer, OrdersSerializer, ProfilesTypeSerializer, BaseInfoSerializer, OrderCountSerializer
from market_app.models import Profiles, Offers, OffersDetails, Reviews, Orders
from rest_framework import generics, status
from rest_framework.views import APIView 
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, AllowAny
from .premissions import IsOwnerOrAdmin
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from market_app.filter import OfferFilter, ReviewFilter
from rest_framework.filters import SearchFilter
from django.db.models import Q

### Offers ### _________________________________________________________________________

class OffersDetailsViewSet(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        if pk:
            try:
                detail = OffersDetails.objects.get(pk=pk)
                serializer = OffersDetailSerializer(detail)
                return Response(serializer.data)
            except Offers.DoesNotExist:
                return Response({"Error": "Details not found"}, status=status.HTTP_404_NOT_FOUND)
        details = OffersDetails.objects.all()
        serializer = OffersDetailSerializer(details, many=True)
        return Response(serializer.data)


class OfferView(APIView):
    permission_classes = [AllowAny]
    filterset_class = OfferFilter
    search_fields = ['title', 'description']

    def filter_queryset(self, queryset):
        filterset = self.filterset_class(self.request.GET, queryset=queryset)
        if filterset.is_valid():
            queryset = filterset.qs

        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(description__icontains=search_query)
            )
        return queryset

    def post(self, request, *args, **kwargs):
            serializer = CreateOffersSerializer(data=request.data, context={"request": request})
            if serializer.is_valid():
                serializer.save()
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    
    def patch(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        queryset = get_object_or_404(Offers, pk=pk)
        serializer = OffersSerializer(queryset, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    permission_classes = [AllowAny]
    def get(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        if pk:
            try:
                offer = Offers.objects.get(pk=pk)
                serializer = OffersSerializer(offer)
                return Response(serializer.data)
            except Offers.DoesNotExist:
                return Response({"Error": "Offer not found"}, status=status.HTTP_404_NOT_FOUND)
        offers = self.filter_queryset(Offers.objects.all())
        serializer = OffersSerializer(offers, many=True)
        data = {
            'count': offers.count(),
            'results' : serializer.data
        }
        return Response(data)
    
    permission_classes = [IsOwnerOrAdmin]
    def delete(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        queryset = get_object_or_404(Offers, pk=pk)
        queryset.delete()
        return Response({"message": "Offer erfolgreich gelöscht"}, status=status.HTTP_204_NO_CONTENT)
    
### Profiles ### _______________________________________________________________________

class ProfilesFilteredListView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, type, *args, **kwargs):
        if not type in ["business", "customer"]:
            return Response({"error": "type doesn't match for filtering"}, status=status.HTTP_404_NOT_FOUND)
        data = Profiles.objects.filter(type=type)
        if(data):
            serializer = ProfilesTypeSerializer(data, many=True)
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
        

### Reviews ### _______________________________________________________________________
class ReviewsListView(APIView):

    permission_classes = [AllowAny]
    filterset_class = ReviewFilter

    def filter_queryset(self, queryset):
        filterset = self.filterset_class(self.request.GET, queryset=queryset)
        if filterset.is_valid():
            return filterset.qs
        return queryset

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if pk:
            queryset = Reviews.objects.get(pk=pk)
            serializer = ReviewsSerializer(queryset)
            return Response(serializer.data, status=status.HTTP_200_OK)
        queryset = self.filter_queryset(Reviews.objects.all())
        serializer = ReviewsSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        serializer = ReviewsSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        queryset = get_object_or_404(Reviews, pk=pk)
        serializer = ReviewsSerializer(queryset, data= request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        queryset = get_object_or_404(Reviews, pk=pk)
        queryset.delete()
        return Response({"message": "Review erfolgreich gelöscht"}, status=status.HTTP_204_NO_CONTENT)
    

### Reviews ### _______________________________________________________________________
class OrdersListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if pk:
            queryset = get_object_or_404(Orders, pk=pk)
            serializer = OrdersSerializer(queryset)
            return Response(serializer.data, status=status.HTTP_200_OK)
        queryset = Orders.objects.all()
        serializer = OrdersSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        serializer = OrdersSerializer(data= request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        queryset = get_object_or_404(Orders, pk=pk)
        serializer = OrdersSerializer(queryset, data= request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        queryset = get_object_or_404(Orders, pk=pk)
        queryset.delete()
        return Response({"message": "Order erfolgreich gelöscht"}, status=status.HTTP_204_NO_CONTENT)

### order-count ### _______________________________________________________________________
class OrderCountView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        serializer = OrderCountSerializer({}, context={"pk": pk})
        return Response(serializer.data)

### Base-info ### _______________________________________________________________________
class BaseInfoView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, *args, **kwargs):
        serializer = BaseInfoSerializer({})
        return Response(serializer.data)