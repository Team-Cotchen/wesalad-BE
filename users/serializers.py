from rest_framework                  import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from django.db           import transaction
from django.contrib.auth import get_user_model

from characteristics.models      import Answer, Stack
from characteristics.serializers import StackSerializer
from .models                     import UserAnswer, UserStack, GoogleSocialAccount

User = get_user_model()

class UserAnswerSerializer(serializers.ModelSerializer):
    answer = serializers.SerializerMethodField()
    
    def get_answer(self, useranswer):
        data = {
            'content' : useranswer.answer.content,
            'description' : useranswer.answer.description,
        }
        return data
    
    class Meta:
        model = UserAnswer
        fields = ['answer']

class UserStackSerializer(serializers.ModelSerializer):
    stack = StackSerializer(required=False)
    
    class Meta:
        model = UserStack
        fields = ['stack']
        
class GoogleSocialAccountSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = GoogleSocialAccount
        fields = ['sub', 'email', 'image_url']

class UserCreateSerializer(serializers.ModelSerializer): 
    google_account = GoogleSocialAccountSerializer(required=False)
    user_answers   = UserAnswerSerializer(source='useranswers',many=True, required=False)
    user_stacks    = UserStackSerializer(source='userstacks',many=True, required=False)
    token          = serializers.SerializerMethodField()
    
    def get_token(self, user):
        refresh = RefreshToken.for_user(user)
        
        return {
            'refresh': str(refresh),
            'access' : str(refresh.access_token),
        }
        
    @transaction.atomic()
    def create(self, validated_data):
        google_account_id = validated_data.pop('google_account_id')
        stacks            = validated_data.pop('stacks').split(',')
        answers           = validated_data.pop('answers').split(',')
        
        user = User.objects.create(
            name           = validated_data['name'],
            ordinal_number = validated_data['ordinal_number'],
            google_account = GoogleSocialAccount.objects.get(id=google_account_id)
        )
        
        [user.useranswers.create(answer = Answer.objects.get(description=answer)) for answer in answers]
        [user.userstacks.create(stack = Stack.objects.get(title=stack)) for stack in stacks]

        return user
     
    class Meta:
        model  = User
        fields = '__all__'