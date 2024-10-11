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
    path('ansertext/<int:id_a>', views.SocerTextAnswer.as_view(), name="SocerTextAnswer"),
    path('submitanswer/<int:id_q>', views.SubmitAnswer.as_view(), name='submit'),
    path('answercreateJuge/<int:id_a>',views.AnswerCreateJuge.as_view()),
    path('rank/<int:class_id>', views.RankingView.as_view(), name='subcriteria_list'),
    path('Download/<int:file>',views.Download.as_view()),
    path('EditSocerUserGroupView/<int:id_a>',views.EditSocerUserGroupView.as_view()),
    path("RezscoreUser/<int:e_id>",views.RezscoreUser.as_view(), name="RezscoreUser")

]
