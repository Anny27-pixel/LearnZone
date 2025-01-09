from django import forms
from . models import *
from django.forms import widgets




class NotesFrom(forms.ModelForm):
    class Meta:
        model = Notes
        fields = ['title','description']

class HomeworkForm(forms.ModelForm):
    class Meta:
        model = Homework
        fields = ['subject', 'title', 'description', 'due', 'is_finished']
        widgets = {
            'due': widgets.DateInput(attrs={'type': 'date'}),
        }