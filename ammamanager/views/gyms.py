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
from ..forms import GymSignUpForm
from ..models import Gym, User, Fighter, FightOffer


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
        return redirect('gyms:gym_home')


@method_decorator([login_required, gym_required], name='dispatch')
class GymHomeView(ListView):
    model = User
    ordering = ('name', )
    context_object_name = 'gyms'
    template_name = 'ammamanager/gyms/gym_home.html'


@method_decorator([login_required, gym_required], name='dispatch')
class ListFightersView(ListView):
    model = Fighter
    ordering = ('name', )
    context_object_name = 'fighters'
    template_name = 'ammamanager/gyms/fighter_list.html'

    def get_queryset(self):
        query =  self.request.GET.get("q", None)
        queryset = self.request.user.fighters
        if query is not None:
            queryset = queryset.filter(fname__icontains=query)
        return queryset



@method_decorator([login_required, gym_required], name='dispatch')
class FighterCreateView(CreateView):
    model = Fighter
    fields = ('fname', 'lname', 'nname', 'weight', 'wins', 'losses', 'draws', 'nc' )
    template_name = 'ammamanager/gyms/fighter_add_form.html'

    def form_valid(self, form):
        fighter = form.save(commit=False)
        fighter.gym = self.request.user
        fighter.save()
        messages.success(self.request, 'Fighter Successfully Added!!')
        return redirect('gyms:fighter_list')


@login_required
@gym_required
def fighter_view(request, pk, *args, **kwargs):

    fighter = get_object_or_404(Fighter, pk=pk, gym=request.user)
    offers = FightOffer.objects.all()
    offersfighters = offers.filter(fighter = fighter)
    offersopponents = offers.filter(opponent = fighter)
    offers = offersfighters | offersopponents

    return render(request, 'ammamanager/gyms/fighter.html', {
        'fighter' : fighter,
        'offers' : offers
    })


@login_required
@gym_required
def fighter_delete(request, pk):

    Fighter.objects.filter(pk=pk).delete()

    return redirect('gyms:fighter_list')


@login_required
@gym_required
def accept_fight(request, pk, offer_pk):
    fighter = get_object_or_404(Fighter, pk=pk)
    offer = get_object_or_404(FightOffer, pk=offer_pk)
    bout = offer.bout
    offer.accepted = True
    offer.save()

    if fighter == bout.fighter1:
        bout.accepted1 = True
    else:
        bout.accepted2 = True

    bout.save()


    return redirect('gyms:fighter', pk)
