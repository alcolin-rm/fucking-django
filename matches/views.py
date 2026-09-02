from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.db.models import Q, Count
from .models import Match, SportTournament

def match_detail(request, id):
    match = get_object_or_404(Match, id=id)
    return render(request, 'matches/match_detail.html', {'match': match})

def matches_list(request):
    matches = Match.objects.all().order_by('-start_time')
    return render(request, 'matches/match_list.html', {
        'matches': matches,
        'title': 'Все матчи',
    })

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

def matches_future(request):
    now = timezone.now()
    matches = Match.objects.filter(
        start_time__gt=now
    ).order_by('start_time')
    return render(request, 'matches/match_list.html', {
        'matches': matches,
        'title': 'Будущие матчи',
    })

def tournaments_list(request):

    now = timezone.now()
    tournaments = SportTournament.objects.annotate(
        finished_matches=Count('match', filter=Q(match__end_time__lte=now))
    ).order_by('-start_date')
    return render(request, 'matches/tournaments_list.html', {
        'tournaments': tournaments,
    })

def tournament_detail(request, id):

    tournament = get_object_or_404(SportTournament, id=id)
    matches = tournament.match_set.all().order_by('start_time')  
    return render(request, 'matches/tournament_detail.html', {
        'tournament': tournament,
        'matches': matches,
    })