from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.db.models import Q
from .models import Match

# Страница отдельного матча
def match_detail(request, id):
    match = get_object_or_404(Match, id=id)
    return render(request, 'matches/match_detail.html', {'match': match})

# Список всех матчей (от новых к старым)
def matches_list(request):
    matches = Match.objects.all().order_by('-start_time')
    return render(request, 'matches/match_list.html', {
        'matches': matches,
        'title': 'Все матчи',
    })

# Матчи, идущие сейчас (live)
def matches_live(request):
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

# Будущие матчи (ещё не начались)
def matches_future(request):
    now = timezone.now()
    matches = Match.objects.filter(
        start_time__gt=now
    ).order_by('start_time')
    return render(request, 'matches/match_list.html', {
        'matches': matches,
        'title': 'Будущие матчи',
    })