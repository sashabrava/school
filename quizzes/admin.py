from django.contrib import admin
from .models import Quiz,Question,Reply,Result

class ResultAdmin(admin.ModelAdmin):
    readonly_fields = ('date',)
    list_display= ('id','date','quiz','user','score')
    list_filter = ('quiz','user')

@admin.register(Quiz)
class QuizPageAdmin(admin.ModelAdmin):
    search_fields = ['title']

@admin.register(Question)
class QuestionPageAdmin(admin.ModelAdmin):
    list_display= ('id','title','description','explanation')
    search_fields = ['title']

@admin.register(Reply)
class ReplyPageAdmin(admin.ModelAdmin):
    list_display= ('id','title','correct','question')
    list_filter = ('correct',)
    search_fields = ['title', 'question__title']

admin.site.register(Result,ResultAdmin)