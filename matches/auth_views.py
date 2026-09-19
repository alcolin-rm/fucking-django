from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import RegisterForm


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'matches/register.html'
    success_url = reverse_lazy('matches:matches_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        # Автоматически логиним пользователя после регистрации
        login(self.request, self.object)
        return response


class CustomLoginView(LoginView):
    template_name = 'matches/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('matches:matches_list')


def logout_view(request):
    logout(request)
    return redirect('matches:matches_list')