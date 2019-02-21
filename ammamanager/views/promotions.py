from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Avg, Count
from django.forms import inlineformset_factory
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from ..decorators import promotion_required
from ..forms import PromotionSignUpForm, BoutForm, FightForm
from ..models import User, Event, Bout, Fighter, FightOffer, FinishedFight


class PromotionSignUpView(CreateView):
    model = User
    form_class = PromotionSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'promotion'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('promotions:promotion_home')


@method_decorator([login_required, promotion_required], name='dispatch')
class PromotionHomeView(ListView):
    model = User
    ordering = ('name',)
    context_object_name = 'promotions'
    template_name = 'ammamanager/promotions/promotion_home.html'


@method_decorator([login_required, promotion_required], name='dispatch')
class ListEventsView(ListView):
    model = Event
    ordering = ('name', )
    context_object_name = 'events'
    template_name = 'ammamanager/promotions/event_list.html'

    def get_queryset(self):
        queryset = self.request.user.events
        return queryset


@method_decorator([login_required, promotion_required], name='dispatch')
class EventCreateView(CreateView):
    model = Event
    fields = ('name',)
    template_name = 'ammamanager/promotions/event_add_form.html'

    def form_valid(self, form):
        event = form.save(commit=False)
        event.owner = self.request.user
        event.save()
        messages.success(self.request, 'Event Successfully Added!!')
        return redirect('promotions:event_list')


@method_decorator([login_required, promotion_required], name='dispatch')
class EventView(UpdateView):
    model = Event
    fields = ('name',)
    context_object_name = 'event'
    template_name = 'ammamanager/promotions/event.html'

    def get_context_data(self, **kwargs):
        kwargs['bouts'] = self.get_object().bouts.annotate(answers_count=Count('weight'))
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        return self.request.user.events.all()

    def get_success_url(self):
        return reverse('promotions:event', kwargs={'pk': self.object.pk})


@login_required
@promotion_required
def finished_event(request, pk):
    event = get_object_or_404(Event, pk=pk, owner=request.user)
    bouts = Bout.objects.all().filter(event=event)
    finished = FinishedFight.objects.all().filter(event=event)

    return render(request, 'ammamanager/promotions/finished_event.html', {
        'event': event,
        'bouts': bouts,
        'finished': finished
    })


@login_required
@promotion_required
def bout_add(request, pk):

    event = get_object_or_404(Event, pk=pk, owner=request.user)

    if request.method == 'POST':
        form = BoutForm(request.POST)
        if form.is_valid():
            bout = form.save(commit=False)
            bout.event = event
            bout.fighter1 = None
            bout.fighter2 = None
            bout.save()
            messages.success(request, 'You may now add fighters to the bout.')
            return redirect('promotions:event', event.pk)
    else:
        form = BoutForm()

    return render(request, 'ammamanager/promotions/bout_add_form.html', {'event': event, 'form': form})





@login_required
@promotion_required
def BoutView(request, pk, bout_pk, *args, **kwargs):

    event = get_object_or_404(Event, pk=pk, owner=request.user)
    bout = get_object_or_404(Bout, pk=bout_pk, event=event)
    fighters = Fighter.objects.all().filter(weight=bout.weight)

    return render(request, 'ammamanager/promotions/bout.html', {
        'event': event,
        'bout' : bout,
        'fighters' : fighters
    })


@login_required
@promotion_required
def offer(request, pk, bout_pk, fighter_pk, *args, **kwargs):

    event = get_object_or_404(Event, pk=pk, owner=request.user)
    bout = get_object_or_404(Bout, pk=bout_pk, event=event)
    fighter = get_object_or_404(Fighter, pk=fighter_pk)

    if (bout.fighter1 == None):
        bout.fighter1 = fighter

    elif (bout.fighter2 == None):
        bout.fighter2 = fighter

    else:
        messages.success(request, 'There are no spaces left in the bout. Please remove a fighter')
    bout.save()

    return redirect('promotions:bout', event.pk, bout.pk)


@login_required
@promotion_required
def offer_fight(request, pk, bout_pk, *args, **kwargs):

    event = get_object_or_404(Event, pk=pk, owner=request.user)
    bout = get_object_or_404(Bout, pk=bout_pk, event=event)
    f1 = bout.fighter1
    f2 = bout.fighter2

    offer1 = FightOffer(fighter = f1, opponent = f2, event = event, bout = bout)

    offer1.save()

    return redirect('promotions:event', event.pk)


@login_required
@promotion_required
def finished_bout(request, pk, bout_pk, fighter_pk):
    bout = get_object_or_404(Bout, pk=bout_pk)
    event = bout.event
    winner = get_object_or_404(Fighter, pk=fighter_pk)

    if request.method == 'POST':
        form = FightForm(request.POST)
        if form.is_valid():
            fight = form.save(commit=False)
            fight.bout = bout
            fight.winner = winner
            fight.event = event
            fight.save()
            fight.bout.final = True
            fight.bout.save()
            winner.wins = winner.wins + 1
            winner.points += 20
            winner.save()
            if winner == bout.fighter1:
                bout.fighter2.losses = bout.fighter2.losses + 1
                bout.fighter2.points -= 10
                bout.fighter2.save()
            else:
                bout.fighter1.losses = bout.fighter1.losses + 1
                bout.fighter1.points -= 10
                bout.fighter1.save()

            messages.success(request, 'Records Updated')
            return redirect('promotions:event', event.pk)
    else:
        form = FightForm()

    return render(request, 'ammamanager/promotions/bout_add_form.html', {'event': event, 'form': form})

@login_required
@promotion_required
def ranking(weight):


    return 0
