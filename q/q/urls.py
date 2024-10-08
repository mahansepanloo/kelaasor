from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls",namespace="accounts")),
    path("class/", include("classs.urls", namespace="classs")),
    path('exercise/',include("exercise.urls",namespace="exercise")),
    path("forum/",include("forum.urls",namespace="forum"))
]
