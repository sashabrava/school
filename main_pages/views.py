from django.shortcuts import render
from django.http import HttpResponse
from .models import StudentProfile
from django.contrib.auth.decorators import login_required

def handler404(request, exception):
    return render(request, 'pages/404.html', status=404)
def handler500(request):
    return render(request, 'pages/500.html', status=500)

def index(request):
    # Main page
    context = {}
    return render(request, 'main_pages/index.html', context)

def contacts(request):
    # Contacts page
    context = {}
    return render(request, 'main_pages/contacts.html', context)

@login_required
def edit_user(request):
    # Page for editing user data from StudentProfile class
    if request.method == 'POST':
        data = request.POST
        request.user.first_name = data['first_name']
        request.user.last_name = data['last_name']
        request.user.email = data['email']
        request.user.save()
    if request.method == 'GET' or request.method == 'POST':
        context = {}
        context['user'] = request.user
        try:
            student_profile = StudentProfile.objects.get(user=request.user)
            context['student_profile'] = student_profile
        except StudentProfile.DoesNotExist:
            student_profile = None
        return render(request, 'main_pages/user-edit.html', context)

def delete_user(request):
    # Page to remove user
    request.user.delete()
    return HttpResponse("Your user has been deleted")