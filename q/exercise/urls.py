from . import views
from django.urls import path

app_name = 'exercise'

urlpatterns = [
    path('create/<int:id_class>', views.CreateExerciseView.as_view(), name='create'),
    path("inbox",views.Inboxew.as_view(), name='inbox'),
    path('edit/<int:id_exercise>', views.EditExerciseView.as_view(), name='edit'),
    path('groupm/<int:id_e>', views.Create_Group_Manual.as_view(), name='groupm'),
    path('score/<int:id_q>', views.SubCriteriaCreate.as_view(), name="SubCriteriaCreate"),
    path('answer/<int:id_q>', views.all_Answer.as_view(), name='answer'),
    path("a/<int:id_q>",views.AllAnswers.as_view()),
    path('ansertext/<int:id_a>', views.SocerTextAnswer.as_view(), name="SocerTextAnswer"),
    path('submitanswer/<int:id_q>', views.SubmitAnswer.as_view(), name='submit'),
    path('answercreateJuge/<int:id_a>',views.AnswerCreateJuge.as_view()),
    path('rank/<int:id_class>', views.RankingView.as_view(), name='subcriteria_list'),
    path('Download/<int:file>',views.Download.as_view()),
    path('EditSocerUserGroupView/<int:id_a>',views.EditSocerUserGroupView.as_view()),
    path("RezscoreUser/<int:e_id>",views.RezscoreUser.as_view(), name="RezscoreUser"),
    path("addtask/<int:e_id>",views.AddTask.as_view(), name="task"),
    path('groups/<int:id_e>/<int:id_class>',views.Show_Groups.as_view(), name='show_groups'),


]
