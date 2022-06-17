from django.http  import HttpResponse, JsonResponse
from django.views import View
from django.db    import transaction
from requests import Response

from characteristics.models import Answer, Stack
from posts.models           import ApplyWay, Category, Post, PostAnswer, PostApplyWay, PostStack
from users.models           import User

class PostListView(View):
    def get(self, request):
        posts = Post.objects.filter()
        
        result = [{
            'id': post.id,
            'user' : {
                'id' : post.user.id,
                'name' : post.user.name,
            },
            'answer' : {
                'id' : [postanswer.answer.id for postanswer in post.postanswers.all()],
                'content' : [postanswer.answer.content for postanswer in post.postanswers.all()],
            },
        } for post in posts]
        
        return JsonResponse({'result' : result}, status=200)