from django.urls import path
from .views import ProfilesListView, ProfilesFilteredListView

urlpatterns = [
    path("profile/<int:pk>/", ProfilesListView.as_view(), name="profile_detail"),
    path("profile/<str:type>/", ProfilesFilteredListView.as_view(), name="profile_business_list"),
]