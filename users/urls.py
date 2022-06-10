from django.urls import path

from users.views import GoogleLoginAPI, GoogleSignInView, SignUpView

urlpatterns = [
    path('/google', GoogleLoginAPI.as_view()),
    path('/signin', GoogleSignInView.as_view()),
    path('/signup/<int:google_account_id>', SignUpView.as_view()),
]
