from django.shortcuts import render
import xhtml2pdf.pisa as pisa
from quizzes.models import Result
from django.conf import settings
from io import BytesIO
from django.template.loader import get_template
from django.http import HttpResponse
from django.views.generic import View
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied

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