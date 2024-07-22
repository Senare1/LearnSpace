from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from functools import wraps
from django.shortcuts import render

def teacher_required(view_func):
    @wraps(view_func)
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and not request.user.is_learner:
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseForbidden("Vous n'êtes pas autorisé à accéder à cette page.")
    return _wrapped_view

