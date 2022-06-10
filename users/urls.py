from django.urls import path

from users.views import GoogleLoginAPI, GoogleSignInView

urlpatterns = [
    path('/google', GoogleLoginAPI.as_view()),
    path('/signin', GoogleSignInView.as_view()),
]
