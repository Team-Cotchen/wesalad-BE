from rest_framework.views    import APIView
from rest_framework.response import Response

from .models     import Post
from .serializer import PostSerializer

class PostListView(APIView):
    def get(self, request):
        posts      = Post.objects.filter()
        serializer = PostSerializer(posts, many=True)
        
        return Response(serializer.data, status=200)