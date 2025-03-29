from django.urls import path
from .views import ProfilesListView, ProfilesFilteredListView, OffersDetailsViewSet, OfferView, ReviewsListView, OrdersListView, BaseInfoView

urlpatterns = [
    path("profile/<int:pk>/", ProfilesListView.as_view(), name="profile_detail"),
    path("profiles/<str:type>/", ProfilesFilteredListView.as_view(), name="profile_business_list"),
    path("offers/", OfferView.as_view(), name="offers_list"),
    path("offers/<int:pk>/", OfferView.as_view(), name="offers_detail"),
    path("offerdetails/<int:pk>/", OffersDetailsViewSet.as_view(), name="offersdetails_detail"),
    path("reviews/", ReviewsListView.as_view(), name="reviews_list"),
    path("reviews/<int:pk>/", ReviewsListView.as_view(), name="reviews_detail"),
    path("orders/", OrdersListView.as_view(), name="orders_list"),
    path("orders/<int:pk>/", OrdersListView.as_view(), name="orders_detail"),
    path("base-info/", BaseInfoView.as_view(), name="base-info")
]