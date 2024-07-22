from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import authenticate
from .models import CustomUser
from courses.models import Matter
from .constants import *


class LearnerForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Nom'})
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Prenom'})
    )
    learner_phone = forms.CharField(
        max_length=15,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Telephone','name':'phone'})
    )
    learner_email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'Email','name':'email'})
    )
    learner_level = forms.ChoiceField(
        choices=LEARNER_LEVEL,
        required=True,
        help_text="Niveau scolaire",
        widget=forms.Select(attrs={'placeholder': 'CLASSE'})
    )

    learner_subscription = forms.ChoiceField(
        choices=LEARNER_SUBCRIPTION,
        required=True,
        help_text="Abonnement standard(100XOF) et premium(150XOF)",
        widget=forms.Select(attrs={'placeholder': 'SOUSCRIPTION'})
    )

    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'}),
    )
    password2 = forms.CharField(
        label="Confirm",
        strip=False,
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm'}),
    )

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'learner_phone', 'learner_email', 'learner_subscription','learner_level', 'password1', 'password2')


class TeacherForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Nom'})
    )

    learner_phone = forms.CharField(
        max_length=15,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Telephone','name':'phone'})
    )
    learner_email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'Email','name':'email'})
    )
    teacher_register = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Matricule'})
    )

    teacher_matter = forms.ChoiceField(
        choices=TEACHER_NAME,
        required=True,
        widget=forms.Select(attrs={'placeholder': 'Matiere enseingée'})
    )

    class Meta:
        model = CustomUser
        fields = ('first_name', 'learner_phone', 'learner_email', 'teacher_matter','teacher_register')




class LearnerLoginForm(forms.Form):
    email_or_phone = forms.CharField(
        max_length=254,
        widget=forms.TextInput(attrs={'placeholder': 'Email ou Téléphone'}),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Mot de passe'}),
    )

    def get_user(self):
        email_or_phone = self.cleaned_data.get('email_or_phone')
        password = self.cleaned_data.get('password')
        user = authenticate(email_or_phone=email_or_phone, password=password)
        return user

class TeacherLoginForm(forms.Form):
    teacher_register = forms.CharField(
        max_length=254,
        widget=forms.TextInput(attrs={'placeholder': 'Matricule'}),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Mot de passe'}),
    )

    def get_user(self):
        teacher_register = self.cleaned_data.get('teacher_register')
        password = self.cleaned_data.get('password')
        user = authenticate(teacher_register=teacher_register, password=password)
        return user




class VerifyForm(forms.Form):
    code = forms.IntegerField()

class PaymentForm(forms.Form):
    choix


#Teacher's form

class AddOneTeacherForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Nom'})
    )
    teacher_register = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'MATRICULE'})
    )
    learner_email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'EMAIL', 'name': 'email'})
    )

    teacher_matter = forms.ModelChoiceField(
        queryset=Matter.objects.all(),
        required=True,
        widget=forms.Select(attrs={'placeholder': 'MATIERE(S)'})
    )

    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={'placeholder': 'PASSWORD'}),
    )
    password2 = forms.CharField(
        label="Confirm",
        strip=False,
        widget=forms.PasswordInput(attrs={'placeholder': 'CONFIRM'}),
    )

    class Meta:
        model = CustomUser
        fields = ('first_name', 'learner_email', 'teacher_register', 'teacher_matter', 'password1', 'password2')


class AddManyTeacherForm(forms.Form):
    first_name = forms.ChoiceField(
        choices=TEACHER_NAME,
        widget=forms.Select(attrs={'placeholder': 'Nom (enseignant)'})
    )
    teacher_register = forms.ChoiceField(
        choices=TEACHER_REGISTER,
        widget=forms.Select(attrs={'placeholder': 'MATRICULE'})
    )

    teacher_email = forms.ChoiceField(
        choices=TEACHER_EMAIL,
        widget=forms.Select(attrs={'placeholder': 'EMAIL', 'name': 'email'})
    )

    teacher_matter = forms.ModelChoiceField(
        queryset=Matter.objects.all(),
        widget=forms.Select(attrs={'placeholder': 'MATIERE(S)'})
    )

    teacher_number = forms.IntegerField(
        required=True,
        widget=forms.NumberInput(attrs={'placeholder': 'NOMBRE'})
    )

    # class Meta:
    #     model = CustomUser
    #     fields = ('first_name', 'learner_email', 'teacher_register', 'teacher_matter', 'teacher_number')



class ProfileForm(forms.Form):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'learner_phone', 'learner_email', 'learner_level', 'learner_subscription')



class PassForm(forms.Form):
    password_1= forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Nouvou mot de passe'}),
    )
    password_2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirmer'}),
    )
    class Meta:
        model = CustomUser
        fields = ["learner_email","password_1","password_2"]

class SearchForm(forms.Form):
    query = forms.CharField(label='search',max_length=100)

# forms.py
from django import forms

# forms.py
from django import forms

class SubscriptionForm(forms.Form):
    PLAN_CHOICES = [
        ('free', 'Free'),
        ('standard', 'Standard'),
        ('premium', 'Premium')
    ]
    plan = forms.ChoiceField(choices=PLAN_CHOICES, widget=forms.RadioSelect)

