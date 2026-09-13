from django import forms
from .models import Match, SportTournament


class MatchForm(forms.ModelForm):
    class Meta:
        model = Match
        fields = [
            'location',
            'start_time',
            'end_time',
            'team1',
            'team2',
            'score1',
            'score2',
            'winner',
            'tournament',
        ]
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def clean(self):
        cleaned = super().clean()
        start = cleaned.get('start_time')
        end = cleaned.get('end_time')
        if start and end and end < start:
            raise forms.ValidationError("Время окончания не может быть раньше времени начала.")
        return cleaned


class SportTournamentForm(forms.ModelForm):
    class Meta:
        model = SportTournament
        fields = ['name', 'start_date', 'end_date']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        cleaned = super().clean()
        start = cleaned.get('start_date')
        end = cleaned.get('end_date')
        if start and end and end < start:
            raise forms.ValidationError("Дата окончания не может быть раньше даты начала.")
        return cleaned