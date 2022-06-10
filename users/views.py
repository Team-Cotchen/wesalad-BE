import jwt, datetime, json

from django.shortcuts import redirect
from django.conf import settings
from django.views import View
from django.http import JsonResponse

from users.models import User
from .services import google_get_access_token, google_get_user_info

class GoogleLoginAPI(View):
    def get(self, request):
        app_key = settings.GOOGLE_OAUTH2_CLIENT_ID
        scope   = "https://www.googleapis.com/auth/userinfo.email " + \
                  "https://www.googleapis.com/auth/userinfo.profile"
        
        redirect_uri    = settings.GOOGLE_OAUTH2_REDIRECT_URI
        google_auth_api = 'https://accounts.google.com/o/oauth2/auth'
        
        response = redirect(f'{google_auth_api}?client_id={app_key}&response_type=code&redirect_uri={redirect_uri}&scope={scope}')
        
        return response

class GoogleSignInView(View):
    def get(self, request):
        auth_code        = request.GET.get('code')
        google_token_api = "https://oauth2.googleapis.com/token"
        body_data = json.loads(request.body)
        
        access_token = google_get_access_token(google_token_api, auth_code)
        user_data    = google_get_user_info(access_token)
        
        google_id              = user_data['sub']
        google_profile_picture = user_data['picture']
        google_email           = user_data['email']
        
        user  = self.get_or_create(body_data, google_id, google_profile_picture, google_email)
        token = self.generate_jwt(user.id)
        
        return JsonResponse({'token' : token}, status=200)
    
    def get_or_create(self, body_data, google_id, google_profile_picture, google_email):
        if not User.objects.filter(google_id=google_id).exists():
            user = User.objects.create(
                name           = body_data['name'],
                ordinal_number = body_data['ordinal_number'],
                email          = google_email,
                image_url      = google_profile_picture,
                google_id      = google_id
            )
        
        user = User.objects.get(google_id=google_id)
        return user
    
    def generate_jwt(self, user_id):
        return jwt.encode({
            'sub': user_id,
            'exp': datetime.datetime.now() + datetime.timedelta(days=1)}, settings.SECRET_KEY, settings.ALGORITHM)