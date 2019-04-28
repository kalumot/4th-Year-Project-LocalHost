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
from django.db.models import Q

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


@login_required
@promotion_required
def promotion_home(request,*args, **kwargs):
    fights = FinishedFight.objects.all().filter(event__owner = request.user)
    ko = 0
    sub = 0
    dec = 0
    draw = 0
    nc = 0
    flw = 0
    bw = 0
    fw = 0
    lw = 0
    ww = 0
    mw = 0
    lhw = 0
    hw = 0
    for f in fights:
        if f.method == 'KO':
            ko += 1
        elif f.method == 'SUB':
            sub += 1
        elif f.method == 'DEC':
            dec += 1
        elif f.method == 'DRAW':
            draw += 1
        elif f.method == 'NC':
            nc += 1
        if f.bout.weight == 'FLW':
            flw += 1
        elif f.bout.weight == 'BW':
            bw += 1
        elif f.bout.weight == 'FW':
            fw += 1
        elif f.bout.weight == 'LW':
            lw += 1
        elif f.bout.weight == 'WW':
            ww += 1
        elif f.bout.weight == 'MW':
            mw += 1
        elif f.bout.weight == 'LHW':
            lhw += 1
        elif f.bout.weight == 'HW':
            hw += 1

    return render(request, 'ammamanager/promotions/promotion_home.html', {
        'KO' : ko,
        'SUB' : sub,
        'DEC' : dec,
        'DRAW': draw,
        'NC': nc,
        'flw': flw,
        'bw': bw,
        'fw': fw,
        'lw': lw,
        'ww': ww,
        'mw': mw,
        'lhw': lhw,
        'hw': hw
    })


@method_decorator([login_required, promotion_required], name='dispatch')
class ListEventsView(ListView):
    model = Event
    ordering = ('name', )
    context_object_name = 'events'
    template_name = 'ammamanager/promotions/event_list.html'
    #events = Event.objects.all().filter(owner=.user)
    def get_queryset(self):
        queryset = self.request.user.events.order_by('-id')
        return queryset


@method_decorator([login_required, promotion_required], name='dispatch')
class EventCreateView(CreateView):
    model = Event
    fields = ('name','date',)
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
def event(request, pk):
    event = get_object_or_404(Event, pk=pk, owner=request.user)
    bouts = Bout.objects.all().filter(event=event)
    finbouts = Bout.objects.all().filter(event=event).filter(set=True).filter(completed=False)
    finished = FinishedFight.objects.all().filter(event=event)
    if event.finished == False:
        return render(request, 'ammamanager/promotions/event.html', {
            'event': event,
            'bouts': bouts,
            'finished': finished
        })
    else:
        return render(request, 'ammamanager/promotions/finished_event.html', {
            'event': event,
            'finbouts': finbouts,
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
    fighters = Fighter.objects.all().filter(weight=bout.weight).filter(available = True)
    recfighterstemp = None;
    if bout.fighter1 is not None:
        fighters = fighters.exclude(pk=bout.fighter1.pk)
        recfighterstemp = fighters.filter(Q(rank=bout.fighter1.rank + 1) | Q(rank=bout.fighter1.rank - 1))

    query =  request.GET.get("q", None)
    if query is not None:
            fighters = fighters.filter(fname__icontains=query)

    return render(request, 'ammamanager/promotions/bout.html', {
        'event': event,
        'bout' : bout,
        'fighters' : fighters,
        'rec' : recfighterstemp
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
def removeFighters(request, pk, bout_pk, *args, **kwargs):

    event = get_object_or_404(Event, pk=pk, owner=request.user)
    bout = get_object_or_404(Bout, pk=bout_pk, event=event)

    bout.fighter1 = None

    bout.fighter2 = None

    bout.save()

    return redirect('promotions:bout', event.pk, bout.pk)

@login_required
@promotion_required
def offer_fight(request, pk, bout_pk, *args, **kwargs):

    event = get_object_or_404(Event, pk=pk, owner=request.user)                    #Doesnt seem right
    bout = get_object_or_404(Bout, pk=bout_pk, event=event)
    f1 = bout.fighter1
    f2 = bout.fighter2
    if f1 is not None and f2 is not None:
        offer1 = FightOffer(fighter = f1, opponent = f2, event = event, bout = bout)
        offer1.save()

    return redirect('promotions:event', event.pk)


@login_required
@promotion_required
def finished_bout(request, pk, bout_pk, fighter_pk):
    bout = get_object_or_404(Bout, pk=bout_pk)
    event = bout.event
    winner = get_object_or_404(Fighter, pk=fighter_pk)
    if bout.fighter1 == winner:
        loser = bout.fighter2
    else:
        loser = bout.fighter1

    if request.method == 'POST':
        form = FightForm(request.POST)
        if form.is_valid():
            fight = form.save(commit=False)
            if fight.method == 'Draw':
                return redirect('promotions:draw_bout', bout.event.pk, bout.pk)
            if fight.method == 'NC':
                return redirect('promotions:nc_bout', bout.event.pk, bout.pk)
            fight.bout = bout
            fight.winner = winner
            fight.loser = loser
            fight.event = event
            fight.save()
            fight.bout.completed = True
            fight.bout.save()

            winner.wins = winner.wins + 1
            loser.losses = loser.losses + 1
            winner.available = True
            loser.available = True
            winner.save()
            loser.save()
            set_fight_scores(fight.id)
            score_fighters()
            ranking(bout.weight)
            messages.success(request, 'Records Updated')
            return redirect('promotions:event', event.pk)
    else:
        form = FightForm()

    return render(request, 'ammamanager/promotions/bout_add_form.html', {'event': event, 'form': form})

def draw_bout(request, pk, bout_pk):
    bout = get_object_or_404(Bout, pk=bout_pk)
    fin = FinishedFight(bout=bout,event = bout.event, winner = bout.fighter1, loser = bout.fighter2, method = 'DRAW', round = 5, min = 5, sec = 0, winnerPoints = 0, loserPoints = 0)
    fin.winner.draws +=1
    fin.winner.available = True
    fin.loser.draws += 1
    fin.loser.available = True
    fin.winner.save()
    fin.loser.save()
    fin.save()
    bout.completed = True
    bout.save()
    return redirect('promotions:event', bout.event.pk)

def nc_bout(request, pk, bout_pk):
    bout = get_object_or_404(Bout, pk=bout_pk)
    fin = FinishedFight(bout=bout,event = bout.event, winner = bout.fighter1, loser = bout.fighter2, method = 'NC', round = 0, min = 0, sec = 0, winnerPoints = 0, loserPoints = 0)
    fin.winner.nc +=1
    fin.winner.available = True
    fin.loser.nc += 1
    fin.loser.available = True
    fin.winner.save()
    fin.loser.save()
    fin.save()
    bout.completed = True
    bout.save()
    return redirect('promotions:event', bout.event.pk)

def finish_event(request, pk):
    event = get_object_or_404(Event, pk=pk)
    offers = FightOffer.objects.all().filter(event=event)
    event.finished = True
    event.save()
    for o in offers:
        o.delete()

    return redirect('promotions:event', event.pk)


def set_fight_scores(pk):
    fin_bout = get_object_or_404(FinishedFight, pk=pk)
    r1 = 10**(fin_bout.winner.points/400)
    r2 = 10**(fin_bout.loser.points/400)
    e1 = r1/(r1 + r2)
    e2 = r2 / (r1 + r2)
    w = 75 * (1 - e1)
    l = 75 * (0 - e2)

    if fin_bout.method is not "DEC":
        w = w * (1 +((6-fin_bout.round)/20))
        l = l * (1 +((6-fin_bout.round)/20))


    fin_bout.winnerPoints = w
    fin_bout.loserPoints = l
    fin_bout.save()
    return 0


def score_fighters():
    fighters = Fighter.objects.all()
    for fighter in fighters:
        points = fighter.initialPointsBoost
        fights = FinishedFight.objects.all().filter(Q(winner=fighter) | Q(loser=fighter))
        for fight in fights:
            if fight.winner == fighter:
                points += fight.winnerPoints
            else:
                points += fight.loserPoints
        fighter.points = 1000 + points
        fighter.save()
    return 0


def ranking(weight):
    fighters = Fighter.objects.all().filter(weight=weight).order_by('-points')
    rank = 1

    for x in fighters:
        x.rank = rank
        rank += 1
        x.save()

    return 0