from django import forms

class QuestionEvaluationForm(forms.Form):
    response = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control','rows':3})
    )