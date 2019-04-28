from django.contrib import admin
from .models import Fighter, FinishedFight, FightOffer, Event, Bout,User


admin.site.register(Fighter)
admin.site.register(FinishedFight)
admin.site.register(FightOffer)
admin.site.register(Event)
admin.site.register(Bout)
admin.site.register(User)


# Register your models here.
