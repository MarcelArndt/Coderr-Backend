from django.urls import path
from .views import ProfilesListView

urlpatterns = [
    path("profile/<int:pk>/", ProfilesListView.as_view(), name="user_detail")
]