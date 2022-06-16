from os import stat
import jwt, datetime, json

from django.shortcuts import redirect
from django.conf      import settings
from django.views     import View
from django.http      import HttpResponse, JsonResponse
from django.db        import IntegrityError

from users.models import User, GoogleSocialAccount
from characteristics.models import Question, Answer, Stack
from .services    import google_get_access_token, google_get_user_info

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
        
        access_token = google_get_access_token(google_token_api, auth_code)
        user_data    = google_get_user_info(access_token)
        
        sub                    = user_data['sub']
        google_profile_picture = user_data['picture']
        google_email           = user_data['email']
        
        google_account = self.get_or_create(sub, google_profile_picture, google_email)
        
        if not User.objects.filter(google_account=google_account).exists():
            return JsonResponse({'google_account_id' : google_account.id})
        
        user  = User.objects.get(google_account=google_account)
        token = self.generate_jwt(user.id)
        
        return JsonResponse({'token' : token}, status=200)

    def get_or_create(self, sub, google_profile_picture, google_email):
        if not GoogleSocialAccount.objects.filter(sub=sub).exists():
            google_account = GoogleSocialAccount.objects.create(
                sub       = sub,
                email     = google_email,
                image_url = google_profile_picture
            )
            return google_account
            
        google_account = GoogleSocialAccount.objects.get(sub=sub)
        return google_account
    
    def generate_jwt(self, user_id):
        return jwt.encode({
            'sub': user_id,
            'exp': datetime.datetime.now() + datetime.timedelta(days=1)}, settings.SECRET_KEY, settings.ALGORITHM)

class SignUpView(View):
    def get(self, request):
        questions = Question.objects.prefetch_related('answers').all()
        result = {
            'characteristics' : [{
                f'question_{question.id}': question.content,
                'answers' : [answer.content for answer in Answer.objects.filter(question=question)]
                } for question in questions],
            
                'stacks' : [{'title' : stack.title, 'image' : stack.image_url} for stack in Stack.objects.all()]
            }
        
        return JsonResponse({'result': result}, status=200)
    
    def post(self, request):
        try: 
            body_data         = json.loads(request.body)
            google_account_id = request.GET.get('google_account_id')
            google_account    = GoogleSocialAccount.objects.get(id=google_account_id)
            
            User.objects.create(
                name           = body_data['name'],
                ordinal_number = body_data['ordinal_number'],
                google_account = google_account
            )
        
            return HttpResponse(status = 201)
        except IntegrityError:
            return JsonResponse({'message' : 'THIS_ACCOUNT_ALREADY_EXIST'}, status=400)