from dataclasses import field, fields
from rest_framework import serializers

from .models import Question, Answer, Stack

class QuestionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Question
        fields = ['content']

class AnswerSerializer(serializers.ModelSerializer):
    question = QuestionSerializer()
    
    class Meta:
        fields = ['content', 'description', 'image_url', 'question']

class StackSerializer(serializers.ModelSerializer):
    
    class Meta:
        fields = ['title', 'description', 'image_url']