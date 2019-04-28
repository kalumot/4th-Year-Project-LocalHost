from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime
from django.utils.html import escape, mark_safe
from django.core.validators import MaxValueValidator


WEIGHT_CLASSES = (
    ('FLW', 'Flyweight'),
    ('BW', 'Bantamweight'),
    ('FW', 'Featherweight'),
    ('LW', 'Lightweight'),
    ('WW', 'Welterweight'),
    ('MW', 'Middleweight'),
    ('LHW', 'Light Heavyweight'),
    ('HW', 'Heavyweight'),
    ('WSW', 'Womens Strawweight'),
    ('WBW', 'Womens Bantamweight'),
    ('WFW', 'Womens Featherweight'),
)

METHODS = (
    ('KO', 'Knock out'),
    ('SUB', 'Submission'),
    ('DEC', 'Decision'),
    ('DRAW', 'Draw'),
    ('NC', 'No Contest'),
)


class User(AbstractUser):
    is_gym = models.BooleanField(default=False)
    is_promotion = models.BooleanField(default=False)


class Gym(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    #interests = models.ManyToManyField(Subject, related_name='interested_gyms')

    def __str__(self):
        return self.user.name


class Event(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='events')
    name = models.CharField(max_length=255)
    date = models.DateField(default=datetime.now())
    finished = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Fighter(models.Model):
    gym = models.ForeignKey(User, on_delete=models.CASCADE, related_name='fighters', null=True)
    fname = models.CharField(max_length=30)
    lname = models.CharField(max_length=30)
    nname = models.CharField(max_length=40)
    weight = models.CharField(max_length=4, choices=WEIGHT_CLASSES, default='FLW')
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    draws = models.IntegerField(default=0)
    nc = models.IntegerField(default=0)
    points = models.IntegerField(default=1000)
    rank = models.IntegerField(default=0)
    available = models.BooleanField(default=True)
    createDate = models.DateField(default=datetime.now())
    initialPointsBoost = models.IntegerField(default=0)

    def __str__(self):
        return self.fname + " " + self.lname


class Bout(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='bouts')
    weight = models.CharField(max_length=4, choices=WEIGHT_CLASSES, default='FLW')
    fighter1 = models.ForeignKey(Fighter, on_delete=models.CASCADE, related_name='f1', blank=True, null=True)
    fighter2 = models.ForeignKey(Fighter, on_delete=models.CASCADE, related_name='f2', blank=True, null=True)
    accepted1 = models.BooleanField(default=False)
    accepted2 = models.BooleanField(default=False)
    set = models.BooleanField(default=False)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.weight


class FightOffer(models.Model):
    bout = models.ForeignKey(Bout,on_delete=models.CASCADE, related_name='bout')
    fighter = models.ForeignKey(Fighter, on_delete=models.CASCADE, related_name='offered_fighter')
    opponent = models.ForeignKey(Fighter, on_delete=models.CASCADE, related_name='opponent', blank=True, null=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='offer_event')
    accepted = models.BooleanField(default=False)

    def __str__(self):
        return self.opponent


class FinishedFight(models.Model):
    bout = models.ForeignKey(Bout,on_delete=models.CASCADE, related_name='finishedbout')
    event = models.ForeignKey(Event,on_delete=models.CASCADE, related_name='finishedevent')
    winner = models.ForeignKey(Fighter, on_delete=models.CASCADE, related_name='winner')
    loser = models.ForeignKey(Fighter, on_delete=models.CASCADE, related_name='loser', default=None)
    method = models.CharField(max_length=5, choices=METHODS, default='DEC')
    round = models.IntegerField(default=1, validators=[MaxValueValidator(5)])
    min = models.IntegerField(default=1)
    sec = models.IntegerField(default=1)
    winnerPoints = models.IntegerField(default=0)
    loserPoints = models.IntegerField(default=0)

    def __str__(self):
        return self.winner
