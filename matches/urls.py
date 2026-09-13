from django.urls import path
from . import views

app_name = 'matches'

urlpatterns = [
    # Публичные страницы матчей
    path('', views.matches_list, name='matches_list'),
    path('live/', views.matches_live, name='matches_live'),
    path('future/', views.matches_future, name='matches_future'),

    # Турниры
    path('tournaments/', views.tournaments_list, name='tournaments_list'),
    path('tournaments/create/', views.tournament_create, name='tournament_create'),
    path('tournaments/edit/<int:id>/', views.tournament_edit, name='tournament_edit'),
    path('tournaments/delete/<int:id>/', views.tournament_delete, name='tournament_delete'),
    path('tournaments/<int:id>/', views.tournament_detail, name='tournament_detail'),

    # CRUD матчей (до <int:id>!)
    path('create/', views.match_create, name='match_create'),
    path('edit/<int:id>/', views.match_edit, name='match_edit'),
    path('delete/<int:id>/', views.match_delete, name='match_delete'),
    path('<int:id>/', views.match_detail, name='match_detail'),
]