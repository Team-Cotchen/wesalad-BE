import jwt

from django.conf import settings
from django.contrib.auth import get_user_model

from rest_framework          import status
from rest_framework.response import  Response

from rest_framework_simplejwt.exceptions  import TokenError
from rest_framework_simplejwt.serializers import TokenRefreshSerializer

User = get_user_model()

def check_token(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            access_token = request.headers.get('access', None)
            payload      = jwt.decode(access_token, settings.SECRET_KEY, settings.ALGORITHM)
            request.user = User.objects.get(id=payload['sub'])

        except jwt.exceptions.ExpiredSignatureError:
            try:
                serializer = TokenRefreshSerializer(data={'refresh': request.headers.get('refresh', None)})
                
                if serializer.is_valid(raise_exception=True): 
                    access_token  = serializer.validated_data['access']
                    refresh_token = request.headers.get('refresh', None)
                
                    return Response({
                        'access' : access_token,
                        'refresh': refresh_token
                    }, status=status.HTTP_200_OK)
                
            except TokenError: 
                return Response({'ERROR': 'Your login has expired.'.upper().replace(' ', '_')},status=status.HTTP_400_BAD_REQUEST)
            except jwt.exceptions.InvalidTokenError: 
                return Response({'ERROR': 'Your login has expired'.upper().replace(' ', '_')}, status=status.HTTP_401_UNAUTHORIZED)
            except User.DoesNotExist:
                return Response({'ERROR': 'USER_DOES_NOT_EXIST'}, status=status.HTTP_400_BAD_REQUEST)        
        
        except jwt.exceptions.DecodeError:
            return Response({'ERROR': 'DECODE_ERROR'}, status=status.HTTP_400_BAD_REQUEST)
        
        return func(self, request, *args, **kwargs)
    return wrapper