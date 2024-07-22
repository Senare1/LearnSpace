from django.urls import path
from . import views

urlpatterns = [
    path('',views.learner_login,name="learner_login"),
    path('teacher_signup/',views.teacher_signup,name="teacher_signup"),
    path('teacher_login/',views.teacher_login,name="teacher_login"),
    path('learner_logout/',views.learner_logout,name="learner_logout"),
    path('teacher_logout/',views.teacher_logout,name="teacher_logout"),

    path('learner_signup/',views.learner_signup,name="learner_signup"),
    path('help/',views.help,name="help"),

    path('help/help_create/',views.help_create,name="help_create"),
    path('help/help_reinitialize/',views.help_reinitialize,name="help_reinitialize"),
    path('help/help_subscribing/',views.help_subscribing,name="help_subscribing"),

    path('verify_email/',views.verify_email,name="verify_email"),
    path('regenerate_code/', views.regenerate_verification_code, name='regenerate_code'),
    path('success/', views.success, name='success'),
    path('learner_signup/failled/', views.failled_subscribing, name='failled'),


    path('signup_one_teacher/',views.signup_one_teacher,name='signup_one_teacher'),
    path('signup_many_teachers/',views.signup_many_teachers,name='signup_many_teachers'),

    path('progress/', views.user_progress, name='user_progress'),
    path('progress/update/', views.update_progress, name='update_progress'),

    path("forgot_verify",views.forgot_verify,name="forgot_verify"),

    path("payment/subscription",views.choose_subscription,name="subscription"),
    path('payment/<int:montant>', views.payment, name='payment'),
    path('payment/success/', views.success, name='success'),
    path('payment/cancel/', views.cancel, name='cancel'),
    path('payment/callback/', views.callback, name='callback'),


]



