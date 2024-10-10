from . import views
from django.urls import path

app_name = 'classs'

urlpatterns = [
    path('class', views.CreateClass.as_view(), name='CreateClass'),
    path('adduser/<int:id_class>',views.AdduserPrivet.as_view(), name='AdduserPrivet'),
    path('addpublic/<int:id_class>',views.AddPublicClass.as_view(),name='AddPublicClass'),
    path('addprivatep/<int:id_class>',views.AddPrivatePassword.as_view(),name="AddPrivatePassword"),
    path('addprivete/<int:id_class>/<str:key>',views.AddPrivateEmailClass.as_view(),name="AddPrivateEmailClass"),
    path('Edite/<int:id_class>',views.Edite.as_view(), name='EditClass'),
    path('subCreateclass/<int:id_class>',views.SubCreateClass.as_view())
]
