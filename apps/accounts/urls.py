from django.urls import path
from .views import RegisterView,LoginView,TestView,ProfileView,AddUserView,UserListView,UserDetailView,LogoutView,ChangePasswordView, ForgotPasswordView,ResetPasswordView


urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view()),
    path("test/", TestView.as_view()),
    path("profile/", ProfileView.as_view()),
    path("add-user/", AddUserView.as_view(), name="add-user"),
    path("users/", UserListView.as_view(), name="user-list"),
    path("users/<int:pk>/", UserDetailView.as_view(), name="user-detail"),
    path("logout/", LogoutView.as_view()),
    path("change-password/", ChangePasswordView.as_view(), name="change-password"),
    path("forgot-password/", ForgotPasswordView.as_view(), name="forgot-password"),
    path("reset-password/", ResetPasswordView.as_view(), name="reset-password"),
]
