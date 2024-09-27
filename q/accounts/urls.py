from . import views
from django.urls import path



app_name = 'accounts'

urlpatterns = [
    path("Register/", views.Register.as_view(), name="register")
]
