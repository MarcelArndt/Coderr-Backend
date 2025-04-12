import django_filters
from .models import Offers, Reviews
from rest_framework.pagination import PageNumberPagination

class OfferFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name="min_price", lookup_expr='gte')
    max_delivery_time = django_filters.NumberFilter(field_name="min_delivery_time", lookup_expr='lte')
    creator_id = django_filters.NumberFilter(field_name="user__id")
    ordering = django_filters.OrderingFilter(fields=["updated_at", "min_price"])

    class Meta:
        model = Offers
        fields = ['min_price', 'max_delivery_time', 'creator_id', 'ordering']


class ReviewFilter(django_filters.FilterSet):
    ordering = django_filters.OrderingFilter(fields=["updated_at", "rating"])
    business_user_id = django_filters.NumberFilter(field_name="business_user__id")
    reviewer_id = django_filters.NumberFilter(field_name="reviewer__id")

    class Meta:
        model = Reviews
        fields = ['reviewer_id', 'business_user_id', 'ordering']


class OffersDetailsPaginationFilter(PageNumberPagination):
    page_size = 6 
    page_size_query_param = 'page_size' 
    max_page_size = 10  