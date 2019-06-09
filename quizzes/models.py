from django.db import models
from django.db.models import Q
from rest_framework import serializers
from django.contrib.auth.models import User
from main_pages.models import StudentGroup


class Question(models.Model):
    # Class 
    title = models.CharField(max_length=100,blank=False)
    description = models.CharField(max_length=100,blank=True)
    explanation = models.CharField(max_length=100,blank=True)
    def correct_replies(self):
        return Reply.objects.filter(Q(question=self) & Q(correct=True))
    def __str__(self):
        return self.title

class Quiz(models.Model):
    # Class for storing info about quiz
    title = models.CharField(max_length=100,blank=False)
    description = models.CharField(max_length=100,blank=True)
    questions = models.ManyToManyField(Question, blank=True)
    auth_required = models.BooleanField(default=False)
    student_groups = models.ManyToManyField(StudentGroup,blank=True)
    def __str__(self):
        return self.title

class Reply(models.Model):
    # Class for storing replies on question
    title = models.CharField(max_length=100,blank=False)
    correct = models.BooleanField(default=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.question) + "-" + self.title

class Result(models.Model):
    # Class for storing results of quizes
    score = models.DecimalField(max_digits=7, decimal_places=2, default=0) # TODO: create function that counts quiz score
    replies = models.ManyToManyField(Reply, blank=True)
    json = models.TextField(blank=True)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, blank=True)
    session_key = models.CharField(max_length=100,blank=True)
    user = models.ForeignKey(User, blank=True,null=True,on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True, blank=True)
    def __str__(self):
        return str(self.id) + ". Quiz " + self.quiz.title + str(self.date )

class QuizModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = "__all__"
