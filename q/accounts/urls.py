from . import views
from django.urls import path



app_name = 'accounts'

urlpatterns = [
    path("Register", views.Register.as_view(), name="register"),
    path('login', views.LoginView.as_view(),name="login"),
    path('refresh', views.RefreshView.as_view(), name="refresh"),
    path('optcode', views.OptCode.as_view(), name="OptCode"),
    path('Change_password', views.Change_password.as_view(), name="Change_password"),
    path('Change_password2', views.Change_password2.as_view(), name="Change_password2"),
    path('profile', views.EditUser.as_view(), name="profile"),
    path('profilesocer', views.UserSocer.as_view(), name='s'),
    path('GetSocerINclass/<int:id_class>', views.GetSocerINclass.as_view(), name='GetSocerINclass')

]
