from rest_framework.views       import APIView
from rest_framework.response    import Response
from rest_framework.permissions import IsAuthenticated

from .models     import Post
from .serializers import PostCreateSerializer, PostDetailSerializer, PostSimpleSerializer

class PostSimpleView(APIView):
    def get(self, request):
        posts      = Post.objects.all()
        serializer = PostSimpleSerializer(posts, many=True)
        return Response(serializer.data, status=200)
    
class PostDetailView(APIView):
    def get(self, request, pk):
        try:
            post       = Post.objects.get(id = pk)
            serializer = PostDetailSerializer(post)
            return Response(serializer.data, status=200)
        except Post.DoesNotExist:
            return Response("Post does not exist", status=400)

class PostCreateView(APIView):
    # permission_classes = [IsAuthenticated]
    
    def post(self, request):
        category      = request.data.get("category")
        answers       = request.data.get("answers")
        stacks        = request.data.get("stacks")
        applyway      = request.data.get("applyway")
        applyway_info = request.data.get("applyway_info")
        place         = request.data.get("place")
        flavor        = request.data.get("flavor")
        
        serializer = PostCreateSerializer(data=request.data)
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
