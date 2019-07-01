import os
from django.conf import settings
from docxtpl import DocxTemplate
from celery.decorators import task
from django.urls import reverse
template_path_to_quiz_generate_folder = "generated/quiz/{}"
quiz_filename = "/qiuz.docx"

@task(bind=True)
def async_quiz_docx(self, quiz_serialized):
    doc = DocxTemplate(settings.BASE_DIR + '/info_export/templates/info_export/quiz.docx')
    path_to_quiz_generate_folder = template_path_to_quiz_generate_folder.format(self.request.id)
    path_to_quiz_generate_file = path_to_quiz_generate_folder + quiz_filename
    try:
        if not os.path.exists(os.path.join(settings.MEDIA_ROOT, path_to_quiz_generate_folder)):
                os.makedirs(os.path.join(settings.MEDIA_ROOT, path_to_quiz_generate_folder))
    except OSError:
        print ('Error while reating directory. ' +  os.path.join(settings.MEDIA_ROOT, path_to_quiz_generate_folder))
    context = {'quiz': quiz_serialized}
    doc.render(context)
    doc.save(os.path.join(settings.MEDIA_ROOT, path_to_quiz_generate_file))	
    return reverse('info_export:get-async-file', args=[self.request.id])
@task 
def async_file_remove(folderpath):
    shutil.rmtree(os.path.join(settings.MEDIA_ROOT, folderpath))