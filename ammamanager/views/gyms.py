from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, UpdateView, TemplateView

from ..decorators import gym_required
from ..forms import GymSignUpForm
from ..models import Gym, User, Fighter, FightOffer, Bout, FinishedFight
from django.db.models import Q
import arrow


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
class GymHomeView(TemplateView):
    template_name = 'ammamanager/gyms/gym_home.html'

    def get_context_data(self, **kwargs):
        context = super(GymHomeView, self).get_context_data(**kwargs)
        context['30_day_registrations'] = self.thirty_day_registrations()
        return context

    def thirty_day_registrations(self):
        final_data = []

        date = arrow.now()
        for day in range(1, 30):
            date = date.replace(days=-1)
            count = 5
            final_data.append(count)

        return final_data


@login_required
@gym_required
def gym_home(request,*args, **kwargs):
    fighters = Fighter.objects.all().filter(gym=request.user)
    fights = FinishedFight.objects.all().filter()
    ko = 0
    sub = 0
    dec = 0
    for w in fights:
        if w.winner in fighters:
            if w.method == 'KO':
                ko += 1
            elif w.method == 'SUB':
                sub += 1
            elif w.method == 'DEC':
                dec += 1

    lko = 0
    lsub = 0
    ldec = 0
    for w in fights:
        if w.loser in fighters:
            if w.method == 'KO':
                lko += 1
            elif w.method == 'SUB':
                lsub += 1
            elif w.method == 'DEC':
                ldec += 1

    offered = []
    for f in fighters:
        offers = FightOffer.objects.all().filter(Q(fighter=f) | Q(opponent=f))
        if offers:
            offered.append(f)

    #offered = list(dict.fromkeys(offered))


    return render(request, 'ammamanager/gyms/gym_home.html', {
        'KO' : ko,
        'SUB' : sub,
        'DEC' : dec,
        'lKO': lko,
        'lSUB': lsub,
        'lDEC': ldec,
        'offered': offered
    })


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
        fighter.initialPointsBoost = (20 * fighter.wins) - (20 * fighter.losses)
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
    pastfights = Bout.objects.all().filter(Q(fighter1=fighter) | Q(fighter2=fighter)).order_by('-id')[:1]
    finishedfights = FinishedFight.objects.all().filter(Q(winner=fighter) | Q(loser=fighter)).order_by('-id')
    return render(request, 'ammamanager/gyms/fighter.html', {
        'fighter' : fighter,
        'offers' : offers,
        'past' : pastfights,
        'finished' : finishedfights
    })


@login_required
@gym_required
def fighter_delete(request, pk):

    fighter = get_object_or_404(Fighter, pk=pk)
    fighter.gym = None
    fighter.available = False
    fighter.save()
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

    if bout.accepted1 == True and bout.accepted2 == True:
        bout.set = True
        offers = FightOffer.objects.all()

        offersfighters1 = offers.filter(fighter=bout.fighter1)
        offersopponents1 = offers.filter(opponent=bout.fighter2)
        offers1 = offersfighters1 | offersopponents1
        for o in offers1:
            if o is not offer:
                o.bout.delete();
            o.delete()

        offersfighters2 = offers.filter(fighter=bout.fighter2)
        offersopponents2 = offers.filter(opponent=bout.fighter1)
        offers1 = offersfighters2 | offersopponents2
        for o in offers1:
            if o is not offer:
                o.bout.delete();
            o.delete()

        bout.fighter1.available = False
        bout.fighter2.available = False
        bout.fighter1.save()
        bout.fighter2.save()

    bout.save()

    return redirect('gyms:fighter', pk)


@login_required
@gym_required
def deny_fight(request, pk, offer_pk):
    fighter = get_object_or_404(Fighter, pk=pk)
    offer = get_object_or_404(FightOffer, pk=offer_pk)
    bout = offer.bout
    offer.delete()
    bout.delete()

    return redirect('gyms:fighter', pk)


@login_required
@gym_required
def fighter_availability(request, pk):
    fighter = get_object_or_404(Fighter, pk=pk)
    if fighter.available == False:
        fighter.available = True
    else:
        fighter.available = False
    fighter.save()
    return redirect('gyms:fighter', pk)


def score_fighters():
    fighters = Fighter.objects.all()
    fights = FinishedFight.objects.all()
    for fighter in fighters:
        points = fighter.initialPointsBoost
        fights = FinishedFight.objects.all().filter(Q(winner=fighter) | Q(loser=fighter))
        for fight in fights:
            if fight.winner == fighter:
                points += fight.winnerPoints
            else:
                points += fight.loserPoints
        fighter.points = 1000 + points;

    return 0