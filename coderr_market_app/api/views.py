from coderr_market_app.api.serializers import ProfilesSerializer, OffersSerializer, OffersDetailSerializer, CreateOffersSerializer, ReviewsSerializer, OrdersSerializer, ProfilesTypeSerializer, BaseInfoSerializer, OrderCountSerializer, completedOrderCountSerializer
from coderr_market_app.models import Profiles, Offers, OffersDetails, Reviews, Orders
from rest_framework import generics, status
from rest_framework.views import APIView 
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated
from .premissions import IsOwnerOrAdmin, IsBusiness, IsCustomer, IsOrderOwnerOrAdmin, IsReviewerOwnerOrAdmin
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from coderr_market_app.filter import OfferFilter, ReviewFilter, OffersDetailsPaginationFilter
from rest_framework.filters import SearchFilter
from django.db.models import Q
from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import ValidationError


### Offers ### _________________________________________________________________________

class OffersDetailsViewSet(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        self.check_permissions(request)
        if pk:
            detail = get_object_or_404(OffersDetails, pk=pk)
            serializer = OffersDetailSerializer(detail)
            return Response(serializer.data)
        details = OffersDetails.objects.all()
        serializer = OffersDetailSerializer(details, many=True)
        return Response(serializer.data)


class OfferView(APIView):
    filterset_class = OfferFilter
    search_fields = ['title', 'description']
    paginator = OffersDetailsPaginationFilter()

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        if self.request.method == 'POST':
            return [IsBusiness()]
        elif self.request.method == 'PATCH' or self.request.method == 'DELETE':
            return [IsOwnerOrAdmin()]
        return super().get_permissions()

    def filter_queryset(self, queryset):
        filterset = self.filterset_class(self.request.GET, queryset=queryset)
        if not filterset.is_valid():
            raise ValidationError(filterset.errors)
        queryset = filterset.qs
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(description__icontains=search_query)
            )
        return  queryset

    def post(self, request, *args, **kwargs):
        self.check_permissions(request)   
        serializer = CreateOffersSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def patch(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        queryset = get_object_or_404(Offers, pk=pk)
        self.check_object_permissions(request, queryset)
        serializer = OffersSerializer(queryset, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        self.check_permissions(request)
        if pk:
            offer = get_object_or_404(Offers, pk=pk)
            serializer = OffersSerializer(offer)
            return Response(serializer.data)
        offers = self.filter_queryset(Offers.objects.all())
        result_page = self.paginator.paginate_queryset(offers, request)
        serializer = OffersSerializer(result_page, many=True)
        data = {
            'count': offers.count(),
            'results' : serializer.data
        }
        return self.paginator.get_paginated_response(serializer.data)
    
    def delete(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        offer = get_object_or_404(Offers, pk=pk)
        self.check_object_permissions(request, offer)
        offer.delete()
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
    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        elif self.request.method == 'PATCH' or self.request.method == 'DELETE':
            return [IsOwnerOrAdmin()]
        return super().get_permissions()

    
    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        user = get_object_or_404(Profiles, pk = pk)
        self.check_permissions(request)  
        serializer = ProfilesSerializer(user)
        data = serializer.data 
        data["user"] = data.pop("id")
        data["created_at"] = data.pop("date_joined")
        return Response(data, status=status.HTTP_200_OK)

        
    def patch(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        queryset = get_object_or_404(Profiles, pk = pk)
        self.check_object_permissions(request, queryset)
        serializer = ProfilesSerializer(queryset, data = request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            data = serializer.data 
            data["user"] = data.pop("id")
            data["created_at"] = data.pop("date_joined")
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        queryset = get_object_or_404(Profiles, pk = pk)
        self.check_object_permissions(request, queryset)
        queryset.delete()
        return Response({"message": "Profil erfolgreich gelöscht"}, status=status.HTTP_204_NO_CONTENT)

### Reviews ### _______________________________________________________________________
class ReviewsListView(APIView):
    filterset_class = ReviewFilter

    def get_permissions(self):
        if self.request.method == 'GET' or self.request.method == 'POST':
            return [IsAuthenticated()]
        elif self.request.method == 'PATCH' or self.request.method == 'DELETE':
            return [IsReviewerOwnerOrAdmin()]
        return super().get_permissions()

    def filter_queryset(self, queryset):
        filterset = self.filterset_class(self.request.GET, queryset=queryset)
        if filterset.is_valid():
            return filterset.qs
        return queryset

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        self.check_permissions(request)   
        if pk:
            queryset = Reviews.objects.get(pk=pk)
            serializer = ReviewsSerializer(queryset)
            return Response(serializer.data, status=status.HTTP_200_OK)
        queryset = self.filter_queryset(Reviews.objects.all())
        serializer = ReviewsSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        self.check_permissions(request)   
        serializer = ReviewsSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        queryset = get_object_or_404(Reviews, pk=pk)
        self.check_object_permissions(request, queryset)
        serializer = ReviewsSerializer(queryset, data= request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        queryset = get_object_or_404(Reviews, pk=pk)
        self.check_object_permissions(request, queryset)
        queryset.delete()
        return Response({"message": "Review erfolgreich gelöscht"}, status=status.HTTP_204_NO_CONTENT)
    

### Orders ### _______________________________________________________________________
class OrdersListView(APIView):

    def get_permissions(self):
        if self.request.method == 'GET' or self.request.method == 'POST':
            return [IsAuthenticated()]
        elif self.request.method == 'PATCH' or self.request.method == 'DELETE':
            return [IsOrderOwnerOrAdmin()]
        return super().get_permissions()

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        self.check_permissions(request)  
        profil = get_object_or_404(Profiles, pk = request.user.id)
        if pk:
            queryset = get_object_or_404(Orders, pk=pk)
            serializer = OrdersSerializer(queryset)
            return Response(serializer.data, status=status.HTTP_200_OK)
        queryset = Orders.objects.filter(Q(offersDetails__offer__user=profil) | Q(user=profil))
        serializer = OrdersSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        self.check_permissions(request)  
        serializer = OrdersSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        queryset = get_object_or_404(Orders, pk=pk)
        self.check_object_permissions(request, queryset)
        serializer = OrdersSerializer(queryset, data=request.data, partial=True, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        queryset = get_object_or_404(Orders, pk=pk)
        self.check_object_permissions(request, queryset)
        queryset.delete()
        return Response({"message": "Order erfolgreich gelöscht"}, status=status.HTTP_204_NO_CONTENT)

### order-count ### _______________________________________________________________________
class OrderCountView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        serializer = OrderCountSerializer({}, context={"pk": pk})
        return Response(serializer.data)

class CompletedOrderCountView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        serializer = completedOrderCountSerializer({}, context={"pk": pk})
        return Response(serializer.data)

### Base-info ### _______________________________________________________________________
class BaseInfoView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, *args, **kwargs):
        serializer = BaseInfoSerializer({})
        return Response(serializer.data)
