from django.urls import path
from .views import UserListView, RegestrationView

urlpatterns = [
    path("login/", UserListView.as_view()),
    path("registration/", RegestrationView.as_view(), name="registration"),
    path("profil/", UserListView.as_view(), name="user_list"),
    path("profil/<int:pk>/", UserListView.as_view(), name="user_detail")
]