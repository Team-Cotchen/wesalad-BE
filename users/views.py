# DRF
from rest_framework.response         import Response
from rest_framework                  import status, generics
from rest_framework.views            import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions      import IsAuthenticated
from rest_framework.decorators       import permission_classes

# Django
from django.shortcuts    import redirect
from django.conf         import settings
from django.contrib.auth import get_user_model

from .models                import GoogleSocialAccount, UserAnswer, UserStack
from characteristics.models import Question, Answer, Stack
from .services              import google_get_access_token, google_get_user_info
from .serializers           import UserCreateSerializer


User = get_user_model()

class GoogleLoginAPI(APIView):
    def get(self, request):
        app_key = settings.GOOGLE_OAUTH2_CLIENT_ID
        scope   = "https://www.googleapis.com/auth/userinfo.email " + \
                  "https://www.googleapis.com/auth/userinfo.profile"
        
        redirect_uri    = settings.GOOGLE_OAUTH2_REDIRECT_URI
        google_auth_api = 'https://accounts.google.com/o/oauth2/auth'
        
        response = redirect(f'{google_auth_api}?client_id={app_key}&response_type=code&redirect_uri={redirect_uri}&scope={scope}')
        return response

class GoogleSignInAPI(APIView):
    def get(self, request):
        auth_code        = request.GET.get('code')
        google_token_api = "https://oauth2.googleapis.com/token"
        
        access_token = google_get_access_token(google_token_api, auth_code)
        user_data    = google_get_user_info(access_token)
        
        google_account, is_created = GoogleSocialAccount.objects.get_or_create(
            sub       = user_data['sub'],
            email     = user_data['email'],
            image_url = user_data['picture']
            )
        if is_created:
            return Response({'google_account' : google_account.id}, status=status.HTTP_200_OK)
        
        if not User.objects.filter(google_account=google_account).exists():
            return Response({'google_account' : google_account.id}, status=status.HTTP_200_OK)
        
        user  = User.objects.get(google_account=google_account)
        token = self.generate_jwt(user)
                
        return Response(token, status=status.HTTP_200_OK)

    # def generate_jwt(self, user_id):
    #     return jwt.encode({
    #         'sub': user_id,
    #         'exp': datetime.datetime.now() + datetime.timedelta(days=30)}, settings.SECRET_KEY, settings.ALGORITHM)
    def generate_jwt(self, user):
        refresh = RefreshToken.for_user(user)
        
        return {
            'refresh': str(refresh),
            'access' : str(refresh.access_token),
        }

class SignUpAPI(generics.CreateAPIView):
        queryset          = User.objects.all()
        lookup_url_kwargs = 'google_account_id'
        
        def create(self, request, *args, **kwargs):
            try:
                serializer = UserCreateSerializer(data = request.data)
                serializer.is_valid(raise_exception=True)
                token = self.perform_create(serializer)
                
                return Response(token, status=status.HTTP_201_CREATED)
            except ValueError:
                return Response({'ERROR' : 'THIS_ACCOUNT_ALREADY_EXIST'}, status=status.HTTP_400_BAD_REQUEST)
        
        def perform_create(self, serializer):
            google_account = GoogleSocialAccount.objects.get(id=self.kwargs.get('google_account_id'))
            
            if not User.objects.filter(google_account = google_account).exists():
                serializer.save(google_account = google_account)
                
                user  = User.objects.get(google_account=google_account)
                token = GoogleSignInAPI.generate_jwt(self, user)
                return token
            raise ValueError

# class UserCharacteristicAPI(APIView):
    

# class SignUpAPI(APIView):
#     def get(self, request):
#         questions = Question.objects.prefetch_related('answers').all()
#         result = {
#             'characteristics' : [{
#                 f'question_{question.id}': question.content,
#                 'answers' : [answer.content for answer in Answer.objects.filter(question=question)]
#                 } for question in questions],
#             
#                 'stacks' : [{'title' : stack.title, 'image' : stack.image_url} for stack in Stack.objects.all()]
#             }
#         
#         return JsonResponse({'result': result}, status=200)
#     
#     def post(self, request):
#         try: 
#             data              = request.POST
#             google_account_id = request.GET.get('google_account_id')
#             google_account    = GoogleSocialAccount.objects.get(id=google_account_id)
#             
#             answers = data['answers'].split(',')
#             stacks  = data['stacks'].split(',')
#             
#             with transaction.atomic():
#                 user = User.objects.create(
#                     name           = data['name'],
#                     ordinal_number = data['ordinal_number'],
#                     google_account = google_account
#                 )
#                 
#                 for answer_id in answers:
#                     UserAnswer.objects.create(
#                         user = user,
#                         answer = Answer.objects.get(id=answer_id)
#                     )
#                 
#                 for stack_id in stacks:
#                     UserStack.objects.create(
#                         user = user,
#                         stack = Stack.objects.get(id=stack_id)
#                     )
# 
#             return HttpResponse(status = 201)
#         except IntegrityError:
#             return JsonResponse({'message' : 'THIS_ACCOUNT_ALREADY_EXIST'}, status=400)
#         except ValueError:
#             return JsonResponse({'message' : 'VALUE_ERROR'}, status=400)

# @permission_classes([IsAuthenticated])
# class FFView(APIView):
#     def get(self, request, *args, **kw):
#         return Response({'s' : 'fds'}, status=status.HTTP_200_OK)