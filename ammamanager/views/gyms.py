from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, UpdateView

from ..decorators import gym_required
from ..forms import GymInterestsForm, GymSignUpForm
from ..models import Gym, User, Fighter


class GymSignUpView(CreateView):
    model = User
    form_class = GymSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'gym'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('gyms:quiz_list')


@method_decorator([login_required, gym_required], name='dispatch')
class QuizListView(ListView):
    model = User
    ordering = ('name', )
    context_object_name = 'quizzes'
    template_name = 'ammamanager/gyms/quiz_list.html'


@method_decorator([login_required, gym_required], name='dispatch')
class ListFightersView(ListView):
    model = Fighter
    ordering = ('name', )
    context_object_name = 'fighters'
    template_name = 'ammamanager/gyms/fighter_list.html'

    def get_queryset(self):
        queryset = self.request.user.fighters
        return queryset

@method_decorator([login_required, gym_required], name='dispatch')
class FighterCreateView(CreateView):
    model = Fighter
    fields = ('fname', 'lname', 'nname', 'wins', 'losses', 'draws', 'nc' )
    template_name = 'ammamanager/gyms/fighter_add_form.html'

    def form_valid(self, form):
        quiz = form.save(commit=False)
        quiz.gym = self.request.user
        quiz.save()
        messages.success(self.request, 'Fighter Successfully Added!!')
        return redirect('gyms:fighter_list')