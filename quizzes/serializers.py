from rest_framework import serializers
from .models import *
class ReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = Reply
        exclude = ()

class QuestionSerializer(serializers.ModelSerializer):
    reply_set  = ReplySerializer(many=True, read_only=True)
    class Meta:
        model = Question
        fields = ('id', 'title', 'description', 'explanation', 'reply_set')

class QuizModelSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)
    class Meta:
        model = Quiz
        fields = "__all__"

class QuizShortModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = ('id', 'title', 'description', 'auth_required')

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