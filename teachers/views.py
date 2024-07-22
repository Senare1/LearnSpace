from django.shortcuts import render, redirect,reverse
from .forms import MediaForm,MediaAddForm,CourseForm,MatterForm, QuestionForm,EvaluationFormUpload,ChallengeForm,TutorialForm,ChapterForm, MediaEditForm,QuestionEditForm,EvaluationEditFom
from courses.models import Course,Challenge,Tutorial,Evaluation,Matter,Chapter,Question,Media
from django.shortcuts import render, get_object_or_404,redirect
from django.contrib import messages
from .decorator import teacher_required
from accounts.models import CustomUser
from accounts.forms import LearnerForm,TeacherForm
from django.forms import inlineformset_factory
from django.db import models



def all_challenges_evaluations_tutorials(teacher):
    matter = teacher.teacher_matter
    tutorials = matter.tutorials.all()
    evaluations = matter.evaluations.all()
    challenges = matter.challenges.all()

    teacher_data = []
    teacher_data.append({
        'matter':matter,
        'tutorials':tutorials,
        'evaluations':evaluations,
        'challenges':challenges,
    })

    return teacher_data
"""
@teacher_required
def teacher_add_evaluation(request):
    if request.method == 'POST':
        form_question = QuestionForm(request.POST)
        if form_question.is_valid():
            evaluation_name = form_question.cleaned_data['evaluation_name']
            teacher_matter = request.user.teacher_matter
            teacher = request.user
            evaluations_exists = Evaluation.objects.filter(models.Q(evaluation_matter=teacher.teacher_matter) |models.Q(evaluation_name=evaluation_name)).exists()
            if not evaluations_exists():
                evaluation = Evaluation(
                    evaluation_name=evaluation_name,
                    evaluation_matter=teacher_matter
                )
                evaluation.save()
                question = form_question.cleaned_data['question']
                response = form_question.cleaned_data['response']
                questions =Question(
                    question=question,
                    response=response,
                    question_evaluation = evaluation
                )
                questions.save()
                return redirect('evaluation')
            else:
                form_question.add_error(None,'Une evaluation de ce contenu existe')
    else:
        form_question = QuestionForm()
        
    context={
        'teacher_data': all_challenges_evaluations_tutorials(request.user)
    }
    return render(request,'teachers/teacher_add_evaluation.html',{'form_question':form_question})

"""


@teacher_required
def teacher_home(request):
    teacher = request.user
    teacher_data = all_challenges_evaluations_tutorials(teacher)

    context = {
        "teacher_data": teacher_data,
    }
    return render(request, "teachers/teacher_home.html", context)

@teacher_required
def teacher_matiere(request):
    teacher = request.user
    teacher_data = all_challenges_evaluations_tutorials(teacher)

    courses = teacher.courses.all()
    context = {
        'teacher_data':teacher_data,
        "teacher": teacher,
        "courses": courses,
    }
    return render(request, "teachers/teacher_matiere.html", context)


@teacher_required
def teacher_course_home(request, slug):
    teacher = request.user

    teacher_data = all_challenges_evaluations_tutorials(teacher)

    course = teacher.courses.get(slug=slug)
    chapters = course.chapters.all()

    context = {
        'teacher_data':teacher_data,
        "teacher": teacher,
        "course": course,
        "chapters": chapters,
    }
    return render(request, "teachers/teacher_course_home.html", context)



@teacher_required
def teacher_course_edit(request, slug):
    teacher = request.user
    course = teacher.courses.get(slug=slug)
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            course_code = form.cleaned_data['course_code']
            course.save()
            messages.success(request, "Le cours a été mis à jour avec succès.")
            return redirect('matiere')
        else:
            messages.error(request, "Veuillez corriger les erreurs ci-dessous.")
    else:
        form = CourseForm(instance=course)
    context = {
        'teacher_data': all_challenges_evaluations_tutorials(teacher),
        'form': form,
        'teacher': teacher,
    }
    return render(request, 'teachers/teacher_course_edit.html', context)


@teacher_required#@login_required_and_is_teacher
def teacher_course_add(request):
    teacher = request.user
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course_title = form.cleaned_data['course_title']
            course_code = form.cleaned_data['course_code']
            course_level = form.cleaned_data['course_level']
            difficulty = form.cleaned_data['difficulty']
            is_premium = form.cleaned_data['is_premium']
            text_content = form.cleaned_data['text_content']
            existing_course = Course.objects.filter(
                models.Q(course_title=course_title) | models.Q(course_code=course_code),
                course_author=teacher
            ).exists()
            if not existing_course:
                course = form.save(commit=False)
                cours = Course(
                    course_title=course_title,
                    course_code=course_code,
                    course_author=teacher,
                    course_level=course_level,
                    course_matter=teacher.teacher_matter,
                    is_premium=is_premium,
                    difficulty=difficulty,
                    text_content=text_content
                )
                cours.save()

                return redirect('matiere')
            else:
                form.add_error('course_title', 'Un cours avec ce titre ou code existe déjà pour vous.')
    else:
        form = CourseForm()


    context = {
        'teacher_data':all_challenges_evaluations_tutorials(teacher),
        'form': form,
        'teacher': teacher,
    }
    return render(request, 'teachers/teacher_course_add.html', context)



@teacher_required
def teacher_course_delete(request, slug):
    teacher = request.user
    
    course = get_object_or_404(Course, slug=slug, course_author=teacher)
    
    instance = course.delete()
    if instance:
        return render(request, 'teachers/deleted_success.html')
    else:
        return render(request, 'teachers/deleted_failled.html')


@teacher_required
def teacher_chapter_home(request, slug, chapter_id):
    teacher = request.user

    course = get_object_or_404(Course, slug=slug, course_author=teacher)
    chapter = Chapter.objects.get(chapter_course=course,id=chapter_id)
    # chapter = get_object_or_404(Chapter, chapter_course=course, chapter_title=chapter_title)
    media = chapter.medias.all()
    context = {
        'teacher_data': all_challenges_evaluations_tutorials(teacher),
        "chapter": chapter,
        "medias": media,
        'course': course
    }
    return render(request, "teachers/teacher_chapter_home.html", context)

"""    if request.method == 'POST':
        form = MediaForm(request.POST,request.FILES)
        if form.is_valid():
            image_media = form.cleaned_data['image_media']
            video_media = form.cleaned_data['video_media']
            document_media = form.cleaned_data['document_media']
            audio_media = form.cleaned_data['audio_media']
            chapter_title = form.cleaned_data['chapter_title']
            content_text = form.cleaned_data['content_text']
            course = teacher.courses.get(slug=slug)
            exists_chapter = Chapter.objects.filter(
                models.Q(chapter_title=chapter_title) | models.Q(chapter_course=course)
            ).exists()
            if not exists_chapter:
                chapter = Chapter(
                    chapter_title=chapter_title,
                    chapter_course=course,
                    content_text=content_text
                )
                chapter.save()
                media = Media(
                    image_media=image_media,
                    document_media=document_media,
                    video_media=video_media,
                    audio_media=add_media,
                    media_chapter=chapter
                )
                media.save()
                return redirect('cours',slug)
            else:
                form.add_error(None,"Un chapitre avec ce contenu existe")
    else:
        form = MediaForm()
    context = {
        'teacher_data':all_challenges_evaluations_tutorials(teacher),
        'form': form,
        'teacher': teacher,
        # 'course':course
            }
    return render(request,"teachers/teacher_chapter_add.html",context)
"""


@teacher_required
def teacher_add_chapter(request,slug):
    teacher = request.user
    course = get_object_or_404(Course, slug=slug, course_author=teacher)
    if request.method == 'POST':
        chapter_form = ChapterForm(request.POST)
        media_form = MediaEditForm(request.POST, request.FILES)
        if chapter_form.is_valid() and media_form.is_valid():
            chapter_title = chapter_form.cleaned_data['chapter_title']
            content_text = chapter_form.cleaned_data['content_text']
            image_media = media_form.cleaned_data['image_media']
            video_media = media_form.cleaned_data['video_media']
            document_media = media_form.cleaned_data['document_media']
            audio_media = media_form.cleaned_data['audio_media']
            chapter = Chapter(
                    chapter_title=chapter_title,
                    chapter_course=course,
                    content_text=content_text
            )
            chapter.save()
            media = Media(
                    image_media=image_media,
                    document_media=document_media,
                    video_media=video_media,
                    audio_media=audio_media,
                    media_chapter=chapter
            )
            media_form.save()
            messages.success(request, "Le chapitre a été mis à jour avec succès.")
            return redirect('cours', slug=slug)
        else:
            messages.error(request, "Veuillez corriger les erreurs ci-dessous.")
    else:
        chapter_form = ChapterForm()
        media_form = MediaEditForm()

    context = {
        'teacher_data': all_challenges_evaluations_tutorials(teacher),
        'chapter_form': chapter_form,
        'media_form': media_form,
        'teacher': teacher,
        'course': course,
    }
    return render(request, "teachers/teacher_add_chapter.html", context)

"""@teacher_required
def teacher_chapter_edit(request, slug, chapter_id):
    teacher = request.user
    course = get_object_or_404(Course, slug=slug, course_author=teacher)
    chapter = get_object_or_404(Chapter, chapter_course=course, id=chapter_id)
    media = get_object_or_404(Media, media_chapter=chapter) 

    if request.method == 'POST':
        chapter_form = ChapterForm(request.POST, instance=chapter)
        media_form = MediaEditForm(request.POST, request.FILES, instance=media)

        if chapter_form.is_valid() and media_form.is_valid():
            chapter_form.save()
            media_form.save()
            messages.success(request, "Le chapitre a été mis à jour avec succès.")
            return redirect('cours', slug=slug)
        else:
            messages.error(request, "Veuillez corriger les erreurs ci-dessous.")
    else:
        chapter_form = ChapterForm(instance=chapter)
        media_form = MediaEditForm(instance=media)

    context = {
        'teacher_data': all_challenges_evaluations_tutorials(teacher),
        'chapter_form': chapter_form,
        'media_form': media_form,
        'teacher': teacher,
        'chapter': chapter,
    }
    return render(request, "teachers/teacher_chapter_edit.html", context)
"""


@teacher_required
def teacher_chapter_edit(request, slug, chapter_id):
    teacher = request.user
    course = get_object_or_404(Course, slug=slug, course_author=teacher)
    chapter = get_object_or_404(Chapter, chapter_course=course, id=chapter_id)
    media = get_object_or_404(Media, media_chapter=chapter) 

    if request.method == 'POST':
        chapter_form = ChapterForm(request.POST, instance=chapter)
        media_form = MediaEditForm(request.POST, request.FILES, instance=media)

        if chapter_form.is_valid() and media_form.is_valid():
            chapter_form.save()
            media_form.save()
            messages.success(request, "Le chapitre a été mis à jour avec succès.")
            return redirect('cours', slug=slug)
        else:
            messages.error(request, "Veuillez corriger les erreurs ci-dessous.")
    else:
        chapter_form = ChapterForm(instance=chapter)
        media_form = MediaEditForm(instance=media)

    context = {
        'teacher_data': all_challenges_evaluations_tutorials(teacher),
        'chapter_form': chapter_form,
        'media_form': media_form,
        'teacher': teacher,
        'chapter': chapter,
    }
    return render(request, "teachers/teacher_chapter_edit.html", context)



@teacher_required
def teacher_add_media_chapter(request, slug, chapter_id):
    teacher = request.user
    course = get_object_or_404(Course, slug=slug, course_author=teacher)
    chapter = get_object_or_404(Chapter, chapter_course=course, id=chapter_id)

    if request.method == 'POST':
        media_form = MediaAddForm(request.POST, request.FILES)

        if media_form.is_valid():
            image_media = media_form.cleaned_data['image_media']
            video_media = media_form.cleaned_data['video_media']
            document_media = media_form.cleaned_data['document_media']
            audio_media = media_form.cleaned_data['audio_media']
            media = Media(
                    image_media=image_media,
                    document_media=document_media,
                    video_media=video_media,
                    audio_media=audio_media,
                    media_chapter=chapter
            )
            media.save()            
            messages.success(request, "Le media a été chargé avec succès.")
            return redirect('chapitre_detail', slug=slug,chapter_id=chapter.id)
        else:
            messages.error(request, "Veuillez corriger les erreurs ci-dessous.")
    else:
        media_form = MediaAddForm()

    context = {
        'teacher_data': all_challenges_evaluations_tutorials(teacher),
        'media_form': media_form,
        'teacher': teacher,
        'chapter': chapter,
    }
    return render(request, "teachers/teacher_add_media_chapter.html", context)


@teacher_required
def teacher_chapter_delete(request,slug,chapter_id):
    teacher = request.user
    course = teacher.courses.get(course_author=teacher,slug=slug)
    chapter =  Chapter.objects.all().get(id=chapter_id)
    instance = chapter.delete()
    if instance:
        return render(request,'teachers/deleted_success.html')
    else:
        return render(request,'teachers/deleted_failled.html')

@teacher_required
def teacher_media_delete(request,slug,chapter_id,media_id):
    teacher = request.user
    course = teacher.courses.get(course_author=teacher,slug=slug)
    chapter = course.chapters.get(id=chapter_id)
    media = chapter.medias.get(media_chapter=chapter,id=media_id)
    instance = media.delete()
    if instance:
        return render(request,'teachers/deleted_success.html')
    else:
        return render(request,'teachers/deleted_failled.html')



@teacher_required
def teacher_text_content(request,slug):
    teacher_text_content = Course.objects.get(slug=slug).text_content()

    return render(request,"teachers/teacher_text_content.html",context={"teacher_text_content":teacher_text_content})




#Views for challenge

@teacher_required
def teacher_challenge(request):
    teacher = request.user
    chal = Challenge.objects.filter(challenge_matter=teacher.teacher_matter)
    context = {
        "teacher_data": all_challenges_evaluations_tutorials(teacher),
        'chal': chal,
        'teacher': teacher
    }
    return render(request,"teachers/teacher_challenge.html",context)



@teacher_required
def teacher_add_challenge(request):
    teacher = request.user
    chal = teacher.teacher_matter.challenges.all()
    if request.method == 'POST':
        form=ChallengeForm(request.POST)
        if form.is_valid():
            challenge_name = form.cleaned_data['challenge_name']
            challenge_image = form.cleaned_data['challenge_image']
            challenge_document = form.cleaned_data['challenge_document']
            if Challenge.objects.filter(challenge_name=challenge_name).exists():
                form.add_error("challenge_name","Un challenge de ce meme contenu existe")
            else:
                challenge = Challenge(
                    challenge_matter=teacher.teacher_matter,
                    challenge_name=challenge_name,
                    challenge_image=challenge_image,
                    challenge_document=challenge_document
                )
                challenge.save()
                return redirect("challenge")
    else:
        form=ChallengeForm()

    context = {
        'teacher_data': all_challenges_evaluations_tutorials(teacher),
        'form': form,
        'teacher': teacher,
        'chal': chal,

    }
    return render(request,"teachers/teacher_add_challenge.html",context)


@teacher_required
def teacher_detail_challenge(request,challenge_id):
    teacher = request.user
    challegnge = Challenge.objects.get(id=challenge_id)
    chal = teacher.teacher_matter.challenges.all()
    if request.method == 'POST':
        form=ChallengeForm(request.POST,request.FILES,instance=challegnge)
        if form.is_valid():
            challenge_name = form.cleaned_data['challenge_name']
            challenge_image = form.cleaned_data['challenge_image']
            challenge_document = form.cleaned_data['challenge_document']
            if Challenge.objects.filter(challenge_name=challenge_name).exists():
                form.add_error("challenge_name","Un challenge de ce meme contenu existe")
            else:

                form.save()
                return redirect("challenge")
    else:
        form=ChallengeForm(instance=challegnge)

    context = {
        'teacher_data': all_challenges_evaluations_tutorials(teacher),
        'form': form,
        'teacher': teacher,
        'chal': chal,

    }
    return render(request,"teachers/teacher_detail_challenge.html",context)


@teacher_required
def teacher_delete_challenge(request,challenge_id):
    challenge = Challenge.objects.filter(id=challenge_id)
    if challenge.exists():
        messages.error(request,"Auccun challenge correspond à ce nom")
        return redirect('challenge')
    else:
        challenge.delete()
        messages.success(request,'Suppression rééussi')
        return redirect('challenge')





#Views for tutorial

@teacher_required
def teacher_tutorial(request):
    teacher = request.user
    tutos = teacher.teacher_matter.tutorials.all()
    context = {
        "teacher_data": all_challenges_evaluations_tutorials(teacher),
        'tutos': tutos,
        'teacher': teacher
    }
    return render(request,"teachers/teacher_tutorial.html",context)


@teacher_required
def teacher_add_tutorial(request):
    teacher = request.user
    if request.method == 'POST':
        form=TutorialForm(request.POST,request.FILES)
        if form.is_valid():
            tutorial_name = form.cleaned_data['tutorial_name']
            tutotrial_videos = form.cleaned_data['tutorial_videos']

            if tutorial.objects.filter(tutorial_name=tutorial_name,tutorial_matter=teacher.teacher_matter).exists():
                form.add_error("tutorial_name","Un tutorial de ce meme contenu existe")
            else:
                tutorial = Tutorial(
                    tutorial_matter=teacher.teacher_matter,
                    tutorial_name=tutorial_name,
                    tutorial_videos=tutotrial_videos
                )
                tutorial.save()
                return redirect("tutorial")
    else:
        form=TutorialForm()
    context = {
            'teacher_data': all_challenges_evaluations_tutorials(teacher),
            'form': form,
            'teacher': teacher
        }
    return render(request,"teachers/teacher_add_tutorial.html",context)



def teacher_delete_tutorial(request,tutorial_name):
    teacher = request.user
    tutorial = teacher.teacher_matter.tutorials.get(tutorial_name=tutorial_name)
    instance = tutorial.delete()
    if not instance:
        messages.error(request,"Auccun tutorial correspond à ce nom")
        return redirect('tutorial')
    else:
        messages.success(request,'Suppression rééussi')
        return render(request,'teachers/deleted_success.html')



#Views for evaluation

@teacher_required
def teacher_evaluation(request):
    teacher = request.user
    evalu = teacher.teacher_matter.evaluations.all()    
    context = {
        'teacher_data': all_challenges_evaluations_tutorials(teacher),
        'evalu': evalu,
        'teacher': teacher
    }
    return render(request,"teachers/teacher_evaluation.html",context)



@teacher_required
def teacher_add_evaluation(request):
    teacher = request.user
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question_text = form.cleaned_data['question']
            response_text = form.cleaned_data['response']
            evaluation_name = form.cleaned_data['evaluation_name']
            
            if Question.objects.filter(question=question_text, response=response_text).exists():
                form.add_error('question', "Question déjà existante")
            else:
                evaluation = Evaluation(evaluation_name=evaluation_name, evaluation_matter=teacher.teacher_matter)
                evaluation.save()
                question = Question(question=question_text, response=response_text, question_evaluation=evaluation)
                question.save()
                return redirect('evaluation')
    else:
        form = QuestionForm()

    context = {
        'teacher_data': all_challenges_evaluations_tutorials(teacher),
        'form': form,
        'teacher': teacher
    }

    return render(request, "teachers/teacher_add_evaluation.html",context)



def teacher_detail_evaluation(request,evaluation_id):
    teacher = request.user
    evaluation = teacher.teacher_matter.evaluations.get(id=evaluation_id)
    question = Question.objects.get(question_evaluation=evaluation)
    if request.method == 'POST':
        form_evaluation = QuestionForm(request.POST,instance=evaluation)
        form_question = QuestionForm(request.POST,instance=question)
        if form_question.is_valid() and form_evaluation.is_valid():
            question_text = form_question.cleaned_data['question']
            response_text = form_question.cleaned_data['response']
            evaluation_name = form_evaluation.cleaned_data['evaluation_name']
            
            if Question.objects.filter(question=question_text, response=response_text).exists():
                form_question.add_error('question', "Question déjà existante")
            else:
                form_evaluation.save()
                form_question.save()
                return redirect('evaluation')
    else:
        form_evaluation = EvaluationEditFom(instance=evaluation)
        form_question = QuestionEditForm(instance=question)

    context = {
        'teacher_data': all_challenges_evaluations_tutorials(teacher),
        'form_question': form_question,
        'form_evaluation': form_evaluation,
        'teacher': teacher
    }

    return render(request, "teachers/teacher_detail_evaluation.html",context)



@teacher_required
def teacher_delete_evaluation(request,evaluation_id):
    evaluation = get_object_or_404(Evaluation,id=evaluation_id)
    if not evaluation:
        messages.error(request,"Auccune evaluation correspond à ce nom")
        return redirect('evaluation')
    else:
        evaluation.delete()
        messages.success(request,'Suppression rééussi')
        return render(request,'teachers/deleted_success.html')


#Other views

def add_learner(request):
    return redirect('learner_signup')

def delete_learner(request, learner_id):
    learner = get_object_or_404(CustomUser, id=learner_id)
    learner.delete()
    messages.success(request, 'L\'élève a été supprimé avec succès.')
    return redirect('list_all_learner')


def list_all_learners(request):
    learners = CustomUser.objects.filter(is_learner=True)
    return render(request, 'teachers/list_all_learners.html', {'learners': learners})


def add_teacher(request):
    return redirect('signup_one_teacher')


def add_many_teachers(request):
    return redirect('signup_many_teachers')


def delete_teacher(request, teacher_id):
    teacher = get_object_or_404(CustomUser, id=teacher_id)
    teacher.delete()
    messages.success(request, 'L\'enseignant a été supprimé avec succès.')
    return redirect('list_all_teacher')


def list_all_teachers(request):
    teachers = CustomUser.objects.filter(is_learner=False)
    return render(request, 'teachers/list_all_teachers.html', {'teachers': teachers})


def detail_learner(request, learner_id):
    learner = get_object_or_404(CustomUser, pk=learner_id, is_learner=True)

    if request.method == 'POST':
        form = LearnerForm(request.POST, instance=learner)
        if form.is_valid():
            form.save()
            messages.success(request, "Profil de l'apprenant mis à jour avec succès.")
            return redirect('detail_learner', learner_id=learner_id)
        else:
            messages.error(request, "Erreur lors de la mise à jour du profil. Veuillez vérifier les informations fournies.")
    else:
        form = LearnerForm(instance=learner)

    return render(request, 'teachers/teacher_detail_learner.html', {'form': form, 'learner': learner})


def detail_teacher(request, teacher_id):
    teacher = get_object_or_404(CustomUser, pk=teacher_id, is_teacher=False)

    if request.method == 'POST':
        form = TeacherForm(request.POST, instance=teacher)
        if form.is_valid():
            form.save()
            messages.success(request, "Profil de l'apprenant mis à jour avec succès.")
            return redirect('detail_teacher', teacher_id=teacher_id)
        else:
            messages.error(request, "Erreur lors de la mise à jour du profil. Veuillez vérifier les informations fournies.")
    else:
        form = TeacherForm()

    return render(request, 'teachers/teacher_detail_teacher.html', {'form': form, 'teacher': teacher})




"""
def add_evaluation(request, matter_id):
    QuestionFormSet = inlineformset_factory(Evaluation, Question, form=QuestionForm, extra=3, can_delete=False)
    matter = get_object_or_404(Matter, pk=matter_id)
    
    if request.method == 'POST':
        evaluation_form = EvaluationForm(request.POST)
        formset = QuestionFormSet(request.POST)
        
        if evaluation_form.is_valid() and formset.is_valid():
            evaluation = evaluation_form.save(commit=False)
            evaluation.evaluation_matter = matter
            evaluation.save()
            questions = formset.save(commit=False)
            for question in questions:
                question.evaluation = evaluation
                question.save()
            
            messages.success(request, "Évaluation et questions enregistrées avec succès.")
            return redirect('some_view_name')
        else:
            messages.error(request, "Erreur lors de l'enregistrement. Veuillez vérifier les informations fournies.")
    else:
        evaluation_form = EvaluationForm(initial={'evaluation_matter': matter})
        formset = QuestionFormSet()
    
    return render(request, 'your_template.html', {
        'evaluation_form': evaluation_form,
        'formset': formset,
        'teacher': matter
    })
"""





"""def uploadQuestion(request,teacher_id):
    matter = get_object_or_404(Matter,pk=teacher_id)
    teacher = get_object_or_404(CustomUser,pk=teacher_id,teacher_matter=matter)
    
    tutorial = Tutorial.objects.all()
    challenge = Challenge.objects.all()
    evaluation = Evaluation.objects.all()

    if request.method == 'POST':
        form = QuestionResponseForm(request.POST)
        if form.is_valid():
            question = form.cleaned_data['question']
            response = form.cleaned_data['response']
            if Question.objects.filter(question=question,response=response).exists():
                form.add_error('question','Cette question existe déjà')
            else:
                form.save()
    else:
        form = QuestionResponseForm()
    return render(request,"teachers/teacher_evaluation.html",{'form':form})"""