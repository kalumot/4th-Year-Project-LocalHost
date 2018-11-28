from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.forms.utils import ValidationError

from ammamanager.models import (Gym, Subject, User)


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
    interests = forms.ModelMultipleChoiceField(
        queryset=Subject.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_gym = True
        user.save()
        gym = Gym.objects.create(user=user)
        gym.interests.add(*self.cleaned_data.get('interests'))
        return user


class GymInterestsForm(forms.ModelForm):
    class Meta:
        model = Gym
        fields = ('interests', )
        widgets = {
            'interests': forms.CheckboxSelectMultiple
        }

