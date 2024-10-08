from django.contrib import admin
from .models import *



@admin.register(AnswersModel)
class AnswersModelAdmin(admin.ModelAdmin):
    pass

@admin.register(ExerciseModel)
class ExerciseModelAdmin(admin.ModelAdmin):
    pass



@admin.register(SubCriteria)
class ModelNameAdmin(admin.ModelAdmin):
    pass

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    pass

@admin.register(GroupAssignment)
class GroupAssignmentAdmin(admin.ModelAdmin):
    pass

@admin.register(RezScore)
class RezScoreAdmin(admin.ModelAdmin):
    pass

@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    pass

@admin.register(Socer)
class SocerAdmin(admin.ModelAdmin):
    pass

@admin.register(InboxExerciseModel)
class InboxExerciseModelAdmin(admin.ModelAdmin):
    pass