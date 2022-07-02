from django.urls import path
from users.views import GoogleLoginAPI, GoogleSignInAPI, SignUpAPI


urlpatterns = [
    path('/google', GoogleLoginAPI.as_view()),
    path('/google/login', GoogleSignInAPI.as_view()),
    path('/signup/<int:google_account_id>', SignUpAPI.as_view()),
]
