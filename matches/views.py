from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from .models import Match

def match_detail(request, id):
    match = get_object_or_404(Match, id=id)
    return render(request, 'matches/match_detail.html', {'match': match})
