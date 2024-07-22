from django.urls import path
from . import views

urlpatterns = [

    path('',views.learner_home,name="learner_home"),
    path("matiere/<str:matter_name>/", views.detail_matiere, name="detail"),
    path("matiere/<str:matter_name>/<slug:slug>/", views.detail_course, name="mon_cours"),
    path("matiere/<str:matter_name>/<slug:slug>/<str:chapter_title>/", views.detail_chapter, name="detail_chapter"),

    path("matiere/<str:matter_name>/<slug:slug>/<str:chapter_title>/<str:course_status>",views.can_download,name="download"),
    path("challenge/<str:challenge_name>/",views.challenge,name="challenge"),
    path("tutorial/<str:tutorial_name>/",views.tutorial,name="tutorial"),

    path("evaluation/<str:evaluation_name>", views.rate_me, name="rate_me"),
]