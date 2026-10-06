from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path("login/", views.StyledLoginView.as_view(), name="login"),
    path("logout/", views.StyledLogoutView.as_view(), name="logout"),

    path("users/", views.UserListView.as_view(), name="user_list"),
    path("users/<int:pk>/", views.UserDetailView.as_view(), name="user_detail"),
    path("users/add/<str:role>/", views.UserCreateView.as_view(), name="user_add"),
    path("users/<int:pk>/edit/", views.UserUpdateView.as_view(), name="user_edit"),
    path("users/<int:pk>/delete/", views.UserDeleteView.as_view(), name="user_delete"),
]
