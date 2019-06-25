from django.shortcuts import render
import xhtml2pdf.pisa as pisa
from quizzes.models import Result, Quiz
from quizzes.serializers import QuizModelSerializer
from django.conf import settings
from io import BytesIO
from django.template.loader import get_template
from django.http import HttpResponse
from django.views.generic import View
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied
from docxtpl import DocxTemplate
from django.http import FileResponse
from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def generate_quiz_docx(request, pk):
    doc = DocxTemplate(settings.BASE_DIR + '/info_export/templates/info_export/quiz.docx')
    quiz = get_object_or_404(Quiz, pk=pk)
    context = {'quiz': QuizModelSerializer(quiz).data}
    doc.render(context)
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    response['Content-Disposition'] = 'attachment; filename=Quiz.docx'
    doc.save(response)
    return response

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