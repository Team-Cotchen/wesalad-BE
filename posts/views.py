from rest_framework             import generics
from rest_framework.views       import APIView
from rest_framework.response    import Response

from utils.utils  import error_message
from .paginations import PostListPagination
from .models      import Post
from .serializers import PostSerializer


class PostListView(generics.ListAPIView):
    queryset         = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = PostListPagination

class PostDetailView(APIView):
    def get(self, request, pk):
        try:
            post       = Post.objects.get(id = pk)
            serializer = PostSerializer(post)
            return Response(serializer.data, status=200)
        except Post.DoesNotExist:
            return Response(error_message("Post does not exist"), status=400)

class PostCreateView(APIView):
    def post(self, request):
        category      = request.data.get("category")
        answers       = request.data.get("answers")
        stacks        = request.data.get("stacks")
        applyway      = request.data.get("applyway")
        applyway_info = request.data.get("applyway_info")
        place         = request.data.get("place")
        flavor        = request.data.get("flavor")
        
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(
                category      = category,
                answers       = answers,
                stacks        = stacks,
                applyway      = applyway,
                applyway_info = applyway_info,
                place         = place,
                flavor        = flavor
            )
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
