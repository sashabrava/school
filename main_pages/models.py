from django.db import models
from django.contrib.auth.models import User

class StudentGroup(models.Model): 
    # Class to keep student group, intended to be sth like "Grade 1"
    title = models.CharField(max_length=140, blank=True, null=True)
    def __str__(self):
        return self.title
def get_user_picture_path(instance, filename):
    # get path for user picture from StudentProfile
    return "users/%s/%s" %(instance.id, filename)
class StudentProfile(models.Model):  
    # Class to keep data about user
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    user_phone = models.CharField(max_length=140, blank=True, null=True)
    user_picture = models.ImageField(upload_to=get_user_picture_path, blank=True, null=True)
    student_groups = models.ManyToManyField(StudentGroup,blank=True)

