from django.shortcuts import render
from django.http import HttpResponse
from .models import Post
from main_pages.models import StudentProfile
from django.contrib.auth.decorators import login_required

def page_posts(request):
    # Page with main school posts
    posts_instance = Post.objects.all()
    context = {'posts':posts_instance}
    return render(request, 'news/news-list.html', context)

def post(request,pk):
    # Page with a certain news post
    # :param int pk: ID of post
    if request.method == 'GET':
        post = Post.objects.get(pk=pk)
        context = {'post':post}
        return render(request, 'news/news.html', context)

