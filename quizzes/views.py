from django.shortcuts import render
from .models import Quiz,Question,Reply,Result,QuizModelSerializer
from main_pages.models import StudentGroup,StudentProfile
from django.http import HttpResponse
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.core.serializers import serialize
import re
from django.db.models import Q
from django.urls import reverse_lazy
from django.contrib.sessions.backends.db import SessionStore
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from io import BytesIO
from django.template.loader import get_template
import xhtml2pdf.pisa as pisa
from django.conf import settings
from lxml import etree
from io import StringIO
from django.contrib.admin.views.decorators import staff_member_required
STATUS_CORRECT = 0
STATUS_PARTLY_CORRECT = 1
STATUS_WRONG = 2

def quizzes(request):
    '''
    Show the list of quizes, available for certain user
    Guest quizes are available as well
    Superuser can see all quizes
    '''
    context = {}
    if request.user.is_superuser:
        quizzes = Quiz.objects.all()
    elif request.user.is_authenticated:
        context['user'] = request.user
        try:
            student_profile = StudentProfile.objects.get(user=request.user)
            context['user_profile'] = student_profile
            quizzes = Quiz.objects.filter(student_groups__in=student_profile.student_groups.all())
        except:
            quizzes = Quiz.objects.filter(student_groups=None)
            print("User_profile can not be found")
    else:
        quizzes = Quiz.objects.filter(auth_required=False)
    context['quizzes'] = quizzes
    return render(request, 'quizzes/quizzes.html', context)

class QuizExistsException(Exception):
    pass

def quiz_upload(request):
    '''
    Function is responsible for showing the upload page and receiving new Quiz
    Importing new quiz should be available only for superuser
    Requirements for quiz:
        Must contain unique title
        Must have a certain XML structure
    '''    
    if request.method == 'GET':
        context = {}
        return render(request, 'quizzes/quiz-upload.html', context)

    if request.method == 'POST':
        result_string = "" # will contain the log of creating new quiz
        myfile = request.FILES['myfile']
        str_text = '' # will contain full text of uploaded file
        for line in myfile:
            str_text = str_text + line.decode()
        tree = etree.parse(StringIO(str_text)) # the free of XML document		
        root = tree.getroot()
        try:
            if root.tag == 'quiz': # main XML tag must be quiz 
                result_string += "Quiz {}{}".format(root.attrib["title"], '\n')
                if len (Quiz.objects.filter(title=root.attrib["title"])) > 0:
                    raise QuizExistsException # if qiuiz with same title exists - abort.
                quiz = Quiz.objects.create()
                quiz.title = root.attrib["title"]
                # find StudentGroup for quiz
                if 'group' in root.attrib:
                    student_group_list = StudentGroup.objects.filter(title=root.attrib["group"] )
                    student_group = None
                    if len(student_group_list) == 1:
                        student_group = student_group_list[0]
                        quiz.student_groups.add(student_group)
                    else:
                        result_string += 'Please, check Student Group on error' + '\n'

                # loop across questions - child evements of root ("quiz") element
                for child in root:
                    result_string += "{} {} {}".format(child.tag, child.attrib, '\n')
                    question_list = Question.objects.filter(title=child.attrib["title"])			
                    if len (question_list) > 0: 
                        result_string += "Question {} exists {}".format(child.attrib["title"], '\n')
                        if len (question_list) == 1: # avoid duplicate questions
                            result_string += "Question  {} will be chosen instead of importable {}".format(question_list[0].id,'\n')
                            quiz.questions.add(question_list[0])
                        continue;
                    question = Question.objects.create()
                    question.title = child.attrib["title"]
                    quiz.questions.add(question)
                    question.save()

                    # loop across replies on question
                    for second_child in child:
                        result_string += "{} {} {}".format(second_child.tag, second_child.attrib, '\n')
                        reply = Reply.objects.create(question=question)
                        reply.title = second_child.text
                        if 'correct' in second_child.attrib and second_child.attrib['correct'] == 'True':
                            reply.correct = True
                        reply.save()
                quiz.save()
        except QuizExistsException:
            result_string += "Quiz {} exists. quitting import{}".format(root.attrib["title"], '\n')
        return JsonResponse({'upload':result_string})

def quiz(request,pk):
    '''
    Show user a quiz
    Session is needed for storing in quiz results
    '''
    if request.session.session_key is None:
        s = SessionStore()
        s.create()
        request.session = s

    quiz = Quiz.objects.get(pk=pk)
    if not request.user.is_authenticated and quiz.auth_required == True:
        #if guest tries to access Quiz for students
        return redirect('login')
    context = {'quiz':quiz}
    print(context)
    return render(request, 'quizzes/quiz.html', context)

@staff_member_required
def edit_quiz(request,pk):
    # page for editing quiz
    if request.method == 'GET':
        quiz = Quiz.objects.get(pk=pk)
        questions_unused = Question.objects.filter(~Q(id__in=quiz.questions.all()))
        context = {'quiz':quiz, 'questions_unused':questions_unused}
        return render(request, 'quizzes/quiz-edit.html', context)
    elif request.method == 'POST':
        quiz_id = int(request.POST.get("quiz-id"))
        quiz = Quiz.objects.get(pk=quiz_id)
        quiz.title = request.POST.get("quiz-title")
        quiz.description = request.POST.get("quiz-description")
        quiz.questions.clear()
        for key, value in request.POST.items():
            if re.match(r'question-added-[0-9]+',key):
                question_id = int(key[15:].split('-')[0])
                question = Question.objects.get(pk=question_id)
                quiz.questions.add(question)
        print(request.POST)
        return HttpResponse(request.POST)

def result(request):
    # page to view and send Result
    if request.method == 'GET':
        pass
    if request.method == 'POST':
        result = Result(json=request.POST)
        quiz_id = int(request.POST.get("quiz-id"))
        result.quiz = Quiz.objects.get(pk=quiz_id)
        if request.session.session_key is not None:
            result.session_key = request.session.session_key
        if request.user.is_authenticated:
            result.user = request.user
        # save raw Result before parsing in order to avoid data loss on error
        result.save()

        for key, value in request.POST.items():
            print(key + " - " + "value")
            if re.match(r'checkbox-[0-9]+-[0-9]+',key):
                question_id = int(key[9:].split('-')[0])
                reply_id = int(key[9:].split('-')[1])
                question = Question.objects.get(pk=question_id)
                reply = Reply.objects.get(pk=reply_id)
                result.replies.add(reply)
                print (" question = " + str(question) + ", answer = " + str(reply))
        result.save()
        context = {'quiz':QuizModelSerializer(result.quiz).data}
        context_full = {**context,**validate_result(result)}
        return JsonResponse(context_full)
    else:
        HttpResponse("Error")
    return HttpResponse("OK!")

def check_replies_on_correct(question_replies, question_correct_replies):
    '''
    Checks replies on certain Question
    :return: Int with code of Reply
    '''
    chosen_correct = [val for val in question_replies if val in question_correct_replies]
    chosen_incorrect = [val for val in question_replies if val not in question_correct_replies]
    if len(chosen_correct) == len(question_correct_replies) and len(chosen_incorrect) == 0:
        return STATUS_CORRECT
    elif len(chosen_correct) == 0:
        return STATUS_WRONG
    else:
        return STATUS_PARTLY_CORRECT


def validate_result(result):
    # Method validates Replies on Quiz
    #:return: JSON with status of Reply on each Question
    result_json = {}
    questions = set() # questions must be taken from quiz, not from reply
    for question in result.quiz.questions.all():
        questions.add(question)
    for question in questions:
        question_replies = list(result.replies.filter(question=question))
        question_correct_replies = list(question.correct_replies())
        result_json[str(question.id)] = check_replies_on_correct(question_replies,question_correct_replies)
    return {'results_checked':result_json}

@login_required
def user_results(request):
    # Page for showing user Results
    user_results = Result.objects.filter(user=request.user)
    context = {'user_results':user_results}
    return render(request, 'quizzes/results.html', context) #20190323 - used to be user_results.html

@login_required
def user_result(request, pk):
    # Page for showing details of single user Result
    user_result = Result.objects.filter(user=request.user, pk=pk)
    context = {}
    if len(user_result) == 1:
        context = {'result':user_result[0]}
    return render(request, 'quizes/result.html', context)

@staff_member_required
def correct_replies(request, pk):
    # Page for viewing correct replies on Quiz
    user_result = Result()
    user_result.quiz = Quiz.objects.get(pk=pk)
    context = {}
    context = {'result':user_result}
    return render(request, 'quizzes/result.html', context)

class UserResultPdf(View):
    # View, which renders test results in PDF format
    def get(self, request,pk):
        user_result = Result.objects.filter(user=request.user, pk=pk)
        params={}
        if len(user_result) == 1:
            params = {
            'result': user_result[0]
            }

        return Render.render(request,'quizes/result_pdf.html', params)    

class Render:
    # Class for static methods of creating PDF
    @staticmethod
    def link_callback(uri, rel):
        '''
        Convert HTML URIs to absolute system paths so xhtml2pdf can access those
        resources
        '''
        # use short variable names
        sUrl = settings.STATIC_URL      # Typically /static/
        sRoot = settings.STATIC_ROOT    # Typically /home/userX/project_static/
        mUrl = settings.MEDIA_URL       # Typically /static/media/
        mRoot = settings.MEDIA_ROOT     # Typically /home/userX/project_static/media/

        # convert URIs to absolute system paths
        if uri.startswith(mUrl):
            path = os.path.join(mRoot, uri.replace(mUrl, ""))
        elif uri.startswith(sUrl):
            path = os.path.join(sRoot, uri.replace(sUrl, ""))
        else:
            return uri  # handle absolute uri (ie: http://some.tld/foo.png)

        # make sure that file exists
        if not os.path.isfile(path):
                raise Exception(
                    'media URI must start with %s or %s' % (sUrl, mUrl)
                )
        return path

    @staticmethod
    def render(request,path: str, params: dict):
        # render PDF document
        template = get_template(path)
        html = template.render(params)
        response = BytesIO()
        pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), response, link_callback=Render.link_callback)
        if not pdf.err:
            return HttpResponse(response.getvalue(), content_type='application/pdf')
        else:
            return HttpResponse("Error Rendering PDF", status=400)