from django.urls import path
from .views import ProfilesListView, ProfilesFilteredListView, OffersViewSet, OffersDetailsViewSet, OfferView

urlpatterns = [
    path("profile/<int:pk>/", ProfilesListView.as_view(), name="profile_detail"),
    path("profile/<str:type>/", ProfilesFilteredListView.as_view(), name="profile_business_list"),
    path("offers/", OfferView.as_view()),
    path("offers-details/", OffersDetailsViewSet.as_view(),)
]