from django.contrib import admin
from .models import *

@admin.register(Classs)
class ClassAdmin(admin.ModelAdmin):
    pass
@admin.register(ListUserPrivet)
class ModelNameAdmin(admin.ModelAdmin):
    pass
