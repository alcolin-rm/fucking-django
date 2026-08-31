from django.urls import path
from . import views

app_name = 'matches'

urlpatterns = [
    path('', views.matches_list, name='matches_list'),
    path('live/', views.matches_live, name='matches_live'),
    path('future/', views.matches_future, name='matches_future'),
    path('tournaments/', views.tournaments_list, name='tournaments_list'),          # список турниров
    path('tournaments/<int:id>/', views.tournament_detail, name='tournament_detail'),  # страница турнира
    path('<int:id>/', views.match_detail, name='match_detail'),                     # страница матча (должна идти последней)
]