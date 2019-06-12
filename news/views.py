from .models import Post
from django.views.generic import ListView, DetailView

class NewsListView(ListView):
    model = Post
class NewsDetailView(DetailView):
    model = Post

