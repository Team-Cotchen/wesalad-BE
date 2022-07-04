from django.urls import path

from posts.views import PostCreateView, PostDetailView, PostSimpleView

urlpatterns = [
    path('', PostSimpleView.as_view()),
    path('/<int:pk>', PostDetailView.as_view()),
    path('/create', PostCreateView.as_view()),
]
