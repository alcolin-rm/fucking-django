from django.urls import path
from . import auth_views

app_name = 'accounts'

urlpatterns = [
    path('register/', auth_views.RegisterView.as_view(), name='register'),
    path('login/', auth_views.CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.logout_view, name='logout'),
]