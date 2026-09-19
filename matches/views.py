from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.db.models import Q, Count
from django.contrib.auth.decorators import user_passes_test
from django.http import JsonResponse

from .models import Match, SportTournament
from .forms import MatchForm, SportTournamentForm


# ---------- Проверка прав ----------

def is_admin(user):
    """Админ — аутентифицированный staff-пользователь."""
    return user.is_authenticated and user.is_staff


admin_required = user_passes_test(is_admin, login_url='/admin/login/')


# ---------- Публичные страницы матчей ----------

def matches_list(request):
    """Список всех матчей от новых к старым."""
    matches = Match.objects.all().order_by('-start_time')
    return render(request, 'matches/match_list.html', {
        'matches': matches,
        'title': 'Все матчи',
    })


def matches_live(request):
    """Матчи, идущие сейчас."""
    now = timezone.now()
    matches = Match.objects.filter(
        start_time__lte=now
    ).filter(
        Q(end_time__gte=now) | Q(end_time__isnull=True)
    ).order_by('start_time')
    return render(request, 'matches/match_list.html', {
        'matches': matches,
        'title': 'Матчи в прямом эфире',
    })


def matches_future(request):
    """Будущие матчи (ещё не начались)."""
    now = timezone.now()
    matches = Match.objects.filter(
        start_time__gt=now
    ).order_by('start_time')
    return render(request, 'matches/match_list.html', {
        'matches': matches,
        'title': 'Будущие матчи',
    })


def match_detail(request, id):
    """Страница отдельного матча."""
    match = get_object_or_404(Match, id=id)
    return render(request, 'matches/match_detail.html', {'match': match})


# ---------- Публичные страницы турниров ----------

def tournaments_list(request):
    """Список турниров с числом завершённых матчей."""
    now = timezone.now()
    tournaments = SportTournament.objects.annotate(
        finished_matches=Count('match', filter=Q(match__end_time__lte=now))
    ).order_by('-start_date')
    return render(request, 'matches/tournaments_list.html', {
        'tournaments': tournaments,
    })


def tournament_detail(request, id):
    """Страница отдельного турнира."""
    tournament = get_object_or_404(SportTournament, id=id)
    matches = tournament.match_set.all().order_by('start_time')
    return render(request, 'matches/tournament_detail.html', {
        'tournament': tournament,
        'matches': matches,
    })


# ---------- CRUD: Матчи (только для админов) ----------

@admin_required
def match_create(request):
    if request.method == 'POST':
        form = MatchForm(request.POST)
        if form.is_valid():
            match = form.save()
            return redirect('matches:match_detail', id=match.id)
    else:
        form = MatchForm()
    return render(request, 'matches/match_form.html', {
        'form': form,
        'title': 'Создание матча',
        'action': 'create',
    })


@admin_required
def match_edit(request, id):
    match = get_object_or_404(Match, id=id)
    if request.method == 'POST':
        form = MatchForm(request.POST, instance=match)
        if form.is_valid():
            form.save()
            return redirect('matches:match_detail', id=match.id)
    else:
        form = MatchForm(instance=match)
    return render(request, 'matches/match_form.html', {
        'form': form,
        'title': f'Редактирование матча #{match.id}',
        'action': 'edit',
        'match': match,
    })


@admin_required
def match_delete(request, id):
    match = get_object_or_404(Match, id=id)
    if request.method == 'POST':
        match.delete()
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'status': 'ok'})
        return redirect('matches:matches_list')
    return render(request, 'matches/match_confirm_delete.html', {'match': match})


# ---------- CRUD: Турниры (только для админов) ----------

@admin_required
def tournament_create(request):
    if request.method == 'POST':
        form = SportTournamentForm(request.POST)
        if form.is_valid():
            tournament = form.save()
            return redirect('matches:tournament_detail', id=tournament.id)
    else:
        form = SportTournamentForm()
    return render(request, 'matches/tournament_form.html', {
        'form': form,
        'title': 'Создание турнира',
        'action': 'create',
    })


@admin_required
def tournament_edit(request, id):
    tournament = get_object_or_404(SportTournament, id=id)
    if request.method == 'POST':
        form = SportTournamentForm(request.POST, instance=tournament)
        if form.is_valid():
            form.save()
            return redirect('matches:tournament_detail', id=tournament.id)
    else:
        form = SportTournamentForm(instance=tournament)
    return render(request, 'matches/tournament_form.html', {
        'form': form,
        'title': f'Редактирование турнира «{tournament.name}»',
        'action': 'edit',
        'tournament': tournament,
    })



@admin_required
def tournament_delete(request, id):
    tournament = get_object_or_404(SportTournament, id=id)
    if request.method == 'POST':
        tournament.delete()
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'status': 'ok'})
        return redirect('matches:tournaments_list')
    return render(request, 'matches/tournament_confirm_delete.html', {
        'tournament': tournament,
    })