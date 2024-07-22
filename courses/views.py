from django.shortcuts import render,get_object_or_404
from .models import Challenge,Chapter,Matter,Course,Tutorial,Evaluation,Question
from django.contrib.auth.decorators import login_required
from accounts.constants import FIRST_CYCLE
from .forms import QuestionEvaluationForm




def all_matters_evaluations_tutorials(learner):
    learner_cycle = learner.is_first_cycle
    if learner_cycle:
        matters = Matter.objects.filter(is_first_cycle=learner_cycle)
    else:
        matters = Matter.objects.all()
    
    matter_data = []
    for matter in matters:
        evaluations = matter.evaluations.all()
        tutorials = matter.tutorials.all()
        challenges = matter.challenges.all()

        matter_data.append({
            'matter': matter,
            'evaluations': evaluations,
            'tutorials': tutorials,
            'challenges': challenges,
        })

    return matter_data


        

@login_required
def learner_home(request):
    learner = request.user
    matters_data = all_matters_evaluations_tutorials(learner)

    context = {
        'matters_data': matters_data,
    }
    return render(request, 'courses/learner_home.html', context)


@login_required
def detail_matiere(request,matter_name):
    learner=request.user
    matters_data = all_matters_evaluations_tutorials(learner)
    is_premium=False
    if learner.learner_subscription == "PREMIUM":
        is_premium = True
    matiere = get_object_or_404(Matter,matter_name=matter_name)
    courses = matiere.courses.all().filter(course_level=learner.learner_level,is_premium=is_premium)

    context = {
        'matters_data': matters_data,
        "courses":courses,
        "matiere": matiere,
    }

    return render(request,"courses/detail_matiere.html",context)


@login_required
def detail_course(request, matter_name, slug):
    learner=request.user
    matters_data = all_matters_evaluations_tutorials(learner)

    matter = get_object_or_404(Matter,matter_name=matter_name)
    course = get_object_or_404(Course,course_matter=matter,slug=slug)
    chapters = course.chapters.all()

    context = {
        'matters_data': matters_data,
        "matiere": matter,
        "course": course,
        "chapters": chapters
    }
    return render(request, "courses/detail_course.html", context)
    

@login_required
def detail_chapter(request, matter_name,slug, chapter_title):
    learner=request.user
    matters_data = all_matters_evaluations_tutorials(learner)
    matter = get_object_or_404(Matter,matter_name=matter_name)
    course = get_object_or_404(Course,course_matter=matter)
    chapters = course.chapters.all()
    chapter = get_object_or_404(Chapter,chapter_matter=course)
    medias = chapter.medias.all()
    context = {
        'matters_data': matters_data,
        "matiere": matter,
        "courses":courses,
        "course": course,
        "chapters": chapters,
        "chapter": chapter,
        'medias': medias
    }

    return render(request, "courses/detail_chapter.html", context)


@login_required
def can_download(request,matter_name,slug,chapter_title,course_status):
    pass

@login_required
def rate_me(request, evaluation_name):
    learner = request.user
    matters_data = all_matters_evaluations_tutorials(learner)
    evaluer = Evaluation.objects.get(evaluation_name=evaluation_name)
    quest = Question.objects.filter(question_evaluation=evaluer).first()
    if request.method == 'POST':
        form = QuestionEvaluationForm(request.POST)
        if form.is_valid():
            form_response = form.cleaned_data['response'].lower()
            # Note: On suppose ici que 'question_evaluation' est la bonne relation
            found = Question.objects.filter(
                question=quest,
                response=form_response,
                question_evaluation=evaluer
            ).exists()

            if found:
                return render(request, 'courses/success.html')
            return render(request, 'courses/failled.html')
    else:
        form = QuestionEvaluationForm()

    context = {
        'matters_data': matters_data,
        'evaluer': evaluer,
        'form': form,
        'quest': quest
    }
    
    return render(request, "courses/my_evaluation.html", context)


@login_required
def challenge(request,challenge_name):
    learner=request.user
    matters_data = all_matters_evaluations_tutorials(learner)

    challenge=get_object_or_404(Challenge,challenge_name=challenge_name)

    context = {
        'matters_data': matters_data,
        "chal":challenge,
    }

    return render(request,"courses/challenge_detail.html")

@login_required
def tutorial(request,tutorial_name):
    learner=request.user
    matters_data = all_matters_evaluations_tutorials(learner)

    matter = get_object_or_404(Matter,matter_name=matter_name)
    courses = matter.courses.all()
    evaluation=get_object_or_404(Evaluation,evaluation_name=evaluation_name)

    context = {
        'matters_data': matters_data,
        "tutorial":tutorial,
    }

    return render(request,"courses/tutorial_detail.html")


@login_required
def search(request,patterns):
    if request.method == 'POST':
        pass

def view_pdf(request,pdf_id):
    pdf = Courses.objects.get()



