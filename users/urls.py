from django.urls import path

from users.views import GoogleLoginAPI, GoogleSignInView, SignUpView

urlpatterns = [
    path('/google', GoogleLoginAPI.as_view()),
    path('/signin', GoogleSignInView.as_view()),
    path('/signup', SignUpView.as_view()),
]
