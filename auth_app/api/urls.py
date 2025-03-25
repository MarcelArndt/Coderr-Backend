from django.urls import path
from .views import UserListView, RegestrationView, LoginView

urlpatterns = [
    path("login/", LoginView.as_view()),
    path("registration/", RegestrationView.as_view(), name="registration"),
    path("profils/", UserListView.as_view(), name="user_list"),
    path("profils/<int:pk>/", UserListView.as_view(), name="user_detail")
]