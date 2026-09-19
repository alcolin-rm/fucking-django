from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Match, SportTournament, Profile


# ---------- Форма матча ----------

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
            'start_time': forms.DateTimeInput(
                attrs={'type': 'datetime-local'},
                format='%Y-%m-%dT%H:%M',
            ),
            'end_time': forms.DateTimeInput(
                attrs={'type': 'datetime-local'},
                format='%Y-%m-%dT%H:%M',
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Чтобы при редактировании поля datetime-local корректно заполнялись
        self.fields['start_time'].input_formats = ['%Y-%m-%dT%H:%M', '%Y-%m-%d %H:%M:%S']
        self.fields['end_time'].input_formats = ['%Y-%m-%dT%H:%M', '%Y-%m-%d %H:%M:%S']

    def clean(self):
        cleaned = super().clean()
        start = cleaned.get('start_time')
        end = cleaned.get('end_time')
        if start and end and end < start:
            raise forms.ValidationError(
                "Время окончания не может быть раньше времени начала."
            )
        return cleaned


# ---------- Форма турнира ----------

class SportTournamentForm(forms.ModelForm):
    class Meta:
        model = SportTournament
        fields = ['name', 'start_date', 'end_date']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'end_date': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['start_date'].input_formats = ['%Y-%m-%d']
        self.fields['end_date'].input_formats = ['%Y-%m-%d']

    def clean(self):
        cleaned = super().clean()
        start = cleaned.get('start_date')
        end = cleaned.get('end_date')
        if start and end and end < start:
            raise forms.ValidationError(
                "Дата окончания не может быть раньше даты начала."
            )
        return cleaned


# ---------- Форма регистрации с аватаром ----------

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=False, label='Email')
    avatar = forms.ImageField(
        required=False,
        label='Аватар',
        widget=forms.FileInput(attrs={'accept': 'image/*'}),
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'avatar')

    def save(self, commit=True):
        user = super().save(commit=commit)
        avatar = self.cleaned_data.get('avatar')
        if avatar:
            profile, _ = Profile.objects.get_or_create(user=user)
            profile.avatar = avatar
            profile.save()
        return user