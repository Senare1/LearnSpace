from django.urls import path
from . import views

urlpatterns = [
    path('',views.teacher_home,name="teacher_home"),
    path('matiere/',views.teacher_matiere,name="matiere"),
    path('matiere/ajouter/',views.teacher_course_add,name="ajouter"),

    path('matiere/<slug:slug>/',views.teacher_course_home,name="cours"),
    path('matiere/<slug:slug>/editer/',views.teacher_course_edit,name="editer"),
    path('matiere/<slug:slug>/retirer/',views.teacher_course_delete,name="retirer"),


    path('matiere/<slug:slug>/chapitre/<int:chapter_id>/', views.teacher_chapter_home, name='chapitre_detail'),
    path('matiere/<slug:slug>/chapitre/<int:chapter_id>/editer/', views.teacher_chapter_edit, name='editer_chapitre'),
    path('matiere/<slug:slug>/chapitre/<int:chapter_id>/ajouter/', views.teacher_add_media_chapter, name='teacher_add_media_chapter'),
    path('matiere/<slug:slug>/chapitre/<int:chapter_id>/retirer/', views.teacher_chapter_delete, name='retirer_chapitre'),
    path('matiere/<slug:slug>/chapitre/<int:chapter_id>/<int:media_id>/retirer', views.teacher_media_delete, name='retirer_media'),
    path('matiere/<slug:slug>/chapitre/ajouter/', views.teacher_add_chapter, name='teacher_add_chapter'),

    path('challenge/',views.teacher_challenge,name="challenge"),
    path('challenge/teacher_add_challenge/',views.teacher_add_challenge,name="teacher_add_challenge"),
    path('challenge/<int:challenge_id>',views.teacher_delete_challenge,name="teacher_delete_challenge"),
    path('challenge/editer/<int:challenge_id>/',views.teacher_detail_challenge,name="teacher_detail_challenge"),

    path('evaluation/',views.teacher_evaluation,name="evaluation"),
    path('evaluation/teacher_add_evaluation/',views.teacher_add_evaluation,name="teacher_add_evaluation"),
    path('evaluation/<int:evaluation_id>/',views.teacher_delete_evaluation,name="teacher_delete_evaluation"),
    path('evaluation/editer/<int:evaluation_id>/',views.teacher_detail_evaluation,name="teacher_detail_evaluation"),

    path('tutorial/',views.teacher_tutorial,name="tutorial"),
    path('tutorial/teacher_add_tutorial/',views.teacher_add_tutorial,name="teacher_add_tutorial"),
    path('tutorial/<str:tutorial_name>/',views.teacher_delete_tutorial,name="teacher_delete_tutorial"),


    path('list_all_learners/',views.list_all_learners,name="list_all_learners"),
    path('list_all_teachers/',views.list_all_teachers,name="list_all_teachers"),
    path('list_all_teachers/<str:learner_id>',views.delete_learner,name="delete_learner"),
    path('delete_teacher/',views.delete_teacher,name="delete_teacher"),

    path("list_all_learners/<str:learner_id>/",views.detail_learner,name="detail_learner"),
    path("list_all_teachers/<str:teacher_id>/",views.detail_teacher,name="detail_teacher")

]