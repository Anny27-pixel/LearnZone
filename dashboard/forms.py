from django import forms
from . models import *


class NotesFrom(forms.ModelForm):
    class Meta:
        model = Notes
        fields = ['title','description']