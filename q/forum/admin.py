from django.contrib import admin
from forum.models import *

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    pass
@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    pass

