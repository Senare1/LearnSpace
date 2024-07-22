from django import forms
from accounts.models import CustomUser
from courses.models import Course, Matter, Media, Evaluation, Challenge, Chapter,Question,Tutorial
from accounts.constants import *

class MatterForm(forms.ModelForm):
    class Meta:
        model = Matter
        fields = ['matter_name',]

class EvaluationFormUpload(forms.ModelForm):
    class Meta:
        model = Evaluation
        fields = ['evaluation_name', 'evaluation_matter']
class EvaluationEditFom(forms.ModelForm):
    class Meta:
        model = Evaluation
        fields = ['evaluation_name']



class QuestionEditForm(forms.ModelForm):
    question = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'placeholder': 'Question',
            'rows':2,
            'class': 'form-control'
            }),
    )
    response = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'placeholder': 'Réponse',
            'rows':2,
            'class': 'form-control'
            }),
    )    
    class Meta:
        model = Question
        fields = ['question', 'response']

class QuestionForm(forms.ModelForm):
    question = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'placeholder': 'Question',
            'rows':2,
            'class': 'form-control'
            }),
    )
    evaluation_name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Nom pour l\'evaluation',
            'class': 'form-control',
        }),
    )
    response = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'placeholder': 'Reponse',
            'rows':2,
            'class': 'form-control',
            }),
    )
    class Meta:
        model = Question
        fields = ['question', 'response','evaluation_name']



class CourseForm(forms.ModelForm):
    course_title = forms.CharField(
        max_length=254,
        widget=forms.TextInput(attrs={'placeholder': 'Titre du cours'}),
    )
    course_code = forms.CharField(
        max_length=32,
        widget=forms.TextInput(attrs={'placeholder': 'Un code pour le cours'}),
    )
    text_content = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'placeholder': 'Rédigez directement','rows':2,'class':'form-control'}),
    )
    course_level = forms.ChoiceField(
        choices=LEARNER_LEVEL,
        widget=forms.Select(attrs={'placeholder': 'Niveau du cours'}),
    )
    is_premium = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'placeholder': 'Cours premium'}),
    )
    difficulty = forms.ChoiceField(
        choices=DIFFICULTY,
        widget=forms.Select(attrs={'placeholder': 'Difficulté'}),
    )

    class Meta:
        model = Course
        fields = ['course_title', 'text_content','course_code', 'course_level', 'is_premium', 'difficulty']


class MediaForm(forms.Form):
    audio_media = forms.FileField(
        required=False,
        widget=forms.ClearableFileInput(attrs={'placeholder': 'Fichier audio','class':'form-control'}),
    )
    video_media = forms.FileField(
        required=False,
        widget=forms.ClearableFileInput(attrs={'placeholder': 'Fichier video','class':'form-control'}),
    )
    document_media = forms.FileField(
        required=False,
        widget=forms.ClearableFileInput(attrs={
            'placeholder': 'Document media','class':'form-control',
        }),
    )
    
    image_media = forms.FileField(
        required=False,
        widget=forms.ClearableFileInput(attrs={'placeholder': 'Fichier image','class':'form-control'}),
    )
    
    chapter_title = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Titre du chapitre',
            'class': 'form-control'
        })
    )
    content_text = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                'placeholder':'Rediger votre chapitre textuellement',
                'rows':2,
                'class':'form-control',
            }
        )
    )



class MediaEditForm(forms.ModelForm):
    audio_media = forms.FileField(
        required=False,
        widget=forms.ClearableFileInput(attrs={'placeholder': 'Fichier audio','class':'form-control'}),
    )
    video_media = forms.FileField(
        required=False,
        widget=forms.ClearableFileInput(attrs={'placeholder': 'Fichier video','class':'form-control'}),
    )
    document_media = forms.FileField(
        required=False,
        widget=forms.ClearableFileInput(attrs={
            'placeholder': 'Document media','class':'form-control',
        }),
    )
    
    image_media = forms.FileField(
        required=False,
        widget=forms.ClearableFileInput(attrs={'placeholder': 'Fichier image','class':'form-control'}),
    )
    
    chapter_title = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Titre du chapitre',
            'class': 'form-control'
        })
    )
    class Meta:
        model=Media
        fields = ['image_media','document_media','video_media','audio_media']


class MediaAddForm(forms.ModelForm):
    audio_media = forms.FileField(
        required=False,
        widget=forms.ClearableFileInput(attrs={'placeholder': 'Fichier audio','class':'form-control'}),
    )
    video_media = forms.FileField(
        required=False,
        widget=forms.ClearableFileInput(attrs={'placeholder': 'Fichier video','class':'form-control'}),
    )
    document_media = forms.FileField(
        required=False,
        widget=forms.ClearableFileInput(attrs={
            'placeholder': 'Document media','class':'form-control',
        }),
    )
    
    image_media = forms.FileField(
        required=False,
        widget=forms.ClearableFileInput(attrs={'placeholder': 'Fichier image','class':'form-control'}),
    )
    
    class Meta:
        model=Media
        fields = ['image_media','document_media','video_media','audio_media']




class ChapterForm(forms.ModelForm):
    chapter_title = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Titre du chapitre',
            'class': 'form-control'
        })
    )
    content_text = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                'placeholder':'Rediger votre chapitre textuellement',
                'rows':2,
                'class':'form-control',
            }
        )
    )
    class Meta:
        model=Chapter
        fields = ['chapter_title','content_text']


class ChallengeForm(forms.ModelForm):
    challenge_name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Nom du tutorial',
            'class': 'form-control'}),
    )
    challenge_document = forms.FileField(
        required=False,
        widget=forms.ClearableFileInput(attrs={
            'placeholder': 'En document',
            'class': 'form-control'
            }),
    )
    challenge_image= forms.FileField(
        required=False,
        widget=forms.ClearableFileInput(attrs={
            'placeholder': 'En image',
            'class': 'form-control'
        }),
    )
    class Meta:
        model = Challenge
        fields = ['challenge_name','challenge_image','challenge_document']


class TutorialForm(forms.Form):
    tutorial_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Nom du tutorial',
            'class': 'form-control'
            }),
    )
    tutorial_videos = forms.FileField(
        required=True,
        widget=forms.ClearableFileInput(attrs={
            'placeholder': 'En vidéos',
            'class': 'form-control'
            }),
    )
    class Meta:
        model = Tutorial
        fields = ['tutorial_name','tutorial_videos']