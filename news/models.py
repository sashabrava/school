from django.db import models
from django.contrib.auth.models import User

def get_post_picture_path(instance, filename):
    return "posts_content/%s/%s" %(instance.id, filename)

class Post(models.Model): 
    # Class that is used to keep data about school news posts 
    title = models.CharField(max_length=200) 
    text = models.TextField() 
    date_created = models.DateTimeField(auto_now_add=True) 
    picture = models.ImageField(upload_to = get_post_picture_path,blank=True, null=True)
    def __str__(self):
        return "Article {}: {}".format(self.date_created.strftime('%Y-%m-%d %H:%M'), self.title )

