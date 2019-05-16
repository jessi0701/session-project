from django import forms
from .models import Score,Movie

class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = "__all__"

class ScoreForm(forms.ModelForm):
    class Meta:
        model = Score
        fields = ['content',]