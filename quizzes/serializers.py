from rest_framework import serializers
from .models import *

class QuizModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = "__all__"
class QuizShortModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = ('id', 'title', 'description', 'auth_required')

class ReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = Reply
        exclude=()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email')

class ResultSerializer(serializers.ModelSerializer):
    replies = ReplySerializer(many=True)
    user = UserSerializer()
    quiz = QuizShortModelSerializer()
    class Meta:
        model = Result
        exclude = ('json',)