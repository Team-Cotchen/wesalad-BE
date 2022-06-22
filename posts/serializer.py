from rest_framework import serializers

from characteristics.models import Answer, Question, Stack
from .models                import (ApplyWay, Category, Place,
                                    Post, PostAnswer, PostApplyWay,
                                    PostPlace, PostStack)


class CategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Category
        fields = ['title']

class PostQuestionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Question
        fields = ['content']

class PostAnswerSerializer(serializers.ModelSerializer):
    question = PostQuestionSerializer()
    
    class Meta:
        model = Answer
        fields = ['question', 'content', 'description', 'image_url']

class PostStackSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Stack
        fields = ['title', 'image_url']

class PostApplyWaySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ApplyWay
        fields = ['title']

class PostPlaceSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Place
        fields = ['title']

class PostAnswerSerializer(serializers.ModelSerializer):
    answer = PostAnswerSerializer(read_only=True)
    
    class Meta:
        model = PostAnswer
        fields = ['is_primary', 'answer']

class PostStackSerializer(serializers.ModelSerializer):
    stack = PostStackSerializer(read_only=True)

    class Meta:
        model = PostStack
        fields = ['stack']

class PostApplyWaySerializer(serializers.ModelSerializer):
    applyway = PostApplyWaySerializer(read_only=True)
    
    class Meta:
        model = PostApplyWay
        fields = ['applyway']
        
class PostPlaceSerializer(serializers.ModelSerializer):
    place = PostPlaceSerializer(read_only=True)
    
    class Meta:
        model = PostPlace
        fields = ['place']

class PostSerializer(serializers.ModelSerializer):
    category      = CategorySerializer()
    post_answer   = PostAnswerSerializer(source='postanswers', many=True)
    post_stack    = PostStackSerializer(source='poststacks', many=True)
    post_applyway = PostApplyWaySerializer(source='postapplyways', many=True)
    post_place    = PostPlaceSerializer(source='postplaces', many=True)
    
    class Meta:
        model  = Post
        fields = '__all__'