from django.db import models

from utils.timestamp        import TimestampZone
from characteristics.models import Stack, Answer

class User(TimestampZone):
    name           = models.CharField(max_length=50)
    email          = models.CharField(max_length=100, unique=True)
    image_url      = models.CharField(max_length=300, null=True, blank=True)
    ordinal_number = models.IntegerField()
    google_id      = models.CharField(max_length=500)
    
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