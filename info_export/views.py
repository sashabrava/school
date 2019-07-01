from django.shortcuts import render
import xhtml2pdf.pisa as pisa
from quizzes.models import Result, Quiz
from django.conf import settings
from io import BytesIO
from django.template.loader import get_template
from django.http import HttpResponse
from django.views.generic import View
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied
from django.http import FileResponse
from django.contrib.admin.views.decorators import staff_member_required
from .tasks import async_quiz_docx, template_path_to_quiz_generate_folder, quiz_filename
from django.http import JsonResponse
from quizzes.serializers import QuizModelSerializer

def get_async_task_status(request, task_id):
    if request.is_ajax():
        result = async_quiz_docx.AsyncResult(task_id)
        if result.ready():
            return JsonResponse({"status": "ready", 'link': result.get()})
        else:
            return JsonResponse({"status": "not ready"})

def get_async_file(request, task_id):
    try:    
        with open(settings.MEDIA_ROOT + "/"+ template_path_to_quiz_generate_folder.format(task_id) + quiz_filename, 'rb') as f:
            file_data = f.read()
            response = HttpResponse(file_data, content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
            response['Content-Disposition'] = 'attachment; filename=Quiz.docx'
            return response
    except IOError:
        # TODO: handle file not exist scenario
        response = HttpResponse('<h1>File not exist</h1>')

@staff_member_required
def generate_quiz_docx(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk)
    async_func = async_quiz_docx.delay(QuizModelSerializer(quiz).data)
    return JsonResponse({"task_id": async_func.task_id})

class UserResultPdf(View):
    # View, which renders test results in PDF format
    def get(self, request,pk):
        user_result = get_object_or_404(Result, pk=pk)
        params={}
        if user_result.user == request.user or request.user.is_staff:
            params = {'result': user_result}
            return Render.render(request,'info_export/result-pdf.html', params)
        raise PermissionDenied    

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