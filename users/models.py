from django.db import models

from utils.timestamp        import TimestampZone
from characteristics.models import Stack, Answer

class GoogleSocialAccount(TimestampZone): 
    sub       = models.CharField(max_length=400)
    image_url = models.CharField(max_length=300, null=True, blank=True)
    email     = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table = 'google_social_accounts'
    
class User(TimestampZone):
    name           = models.CharField(max_length=50)
    ordinal_number = models.IntegerField()
    google_account = models.ForeignKey(GoogleSocialAccount, on_delete=models.CASCADE, unique=True, related_name='users')
    
    class Meta:
        db_table = 'users'

class UserAnswer(TimestampZone):
    user   = models.ForeignKey(User, on_delete=models.CASCADE, related_name='useranswers')
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='useranswers')
    
    class Meta:
        db_table = 'useranswers'

class UserStack(TimestampZone):
    user  = models.ForeignKey(User, on_delete=models.CASCADE, related_name='userstacks')
    stack = models.ForeignKey(Stack, on_delete=models.CASCADE, related_name='userstacks')
    
    class Meta: 
        db_table = 'userstacks'