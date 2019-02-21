from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.forms.utils import ValidationError

from ammamanager.models import (Gym, User, Bout, FinishedFight)


class PromotionSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_promotion = True
        if commit:
            user.save()
        return user


class GymSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_gym = True
        user.save()
        gym = Gym.objects.create(user=user)
        return user


class BoutForm(forms.ModelForm):
    class Meta:
        model = Bout
        fields = ('weight',)


class FightForm(forms.ModelForm):
    class Meta:
        model = FinishedFight
        fields = ('method','round','min','sec',)
