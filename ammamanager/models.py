from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.html import escape, mark_safe


class User(AbstractUser):
    is_gym = models.BooleanField(default=False)
    is_promotion = models.BooleanField(default=False)


class Subject(models.Model):
    name = models.CharField(max_length=30)
    color = models.CharField(max_length=7, default='#007bff')

    def __str__(self):
        return self.name

    def get_html_badge(self):
        name = escape(self.name)
        color = escape(self.color)
        html = '<span class="badge badge-primary" style="background-color: %s">%s</span>' % (color, name)
        return mark_safe(html)


class Gym(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    #interests = models.ManyToManyField(Subject, related_name='interested_gyms')
    Certifications = models.ManyToManyField(Subject, related_name='interested_gyms')


    def __str__(self):
        return self.user.username


class Fighter(models.Model):
    gym = models.ForeignKey(User, on_delete=models.CASCADE, related_name='fighters')
    fname = models.CharField(max_length=30)
    lname = models.CharField(max_length=30)
    nname = models.CharField(max_length=40)
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    draws = models.IntegerField(default=0)
    nc = models.IntegerField(default=0)

    def __str__(self):
        return self.fname + " " + self.lname