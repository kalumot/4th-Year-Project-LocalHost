from django.urls import include, path

from .views import ammamanager, gyms, promotions

urlpatterns = [
    path('', ammamanager.home, name='home'),

    path('gyms/', include(([
        path('', gyms.gym_home, name='gym_home'),
        path('fighters/', gyms.ListFightersView.as_view(), name='fighter_list'),
        path('fighters/<int:pk>', gyms.fighter_view, name='fighter'),
        path('fighters/<int:pk>/<int:offer_pk>/accept', gyms.accept_fight, name='accept_fight'),
        path('fighters/<int:pk>/<int:offer_pk>/deny', gyms.deny_fight, name='deny_fight'),
        path('fighters/<int:pk>/delete', gyms.fighter_delete, name='fighter_delete'),
        path('fighters/<int:pk>/availability', gyms.fighter_availability, name='fighter_availability'),
        path('fighters/add/', gyms.FighterCreateView.as_view(), name='fighter_add'),
    ], 'ammamanager'), namespace='gyms')),


    path('promotions/', include(([
        path('', promotions.promotion_home, name='promotion_home'),
        path('events/', promotions.ListEventsView.as_view(), name='event_list'),
        path('events/add/', promotions.EventCreateView.as_view(), name='event_add'),
        path('events/<int:pk>/', promotions.event, name='event'),
        path('events/<int:pk>/finish', promotions.finish_event, name='finish_event'),
        path('events/<int:pk>/finished', promotions.finished_event, name='finished_event'),
        path('events/<int:pk>/bout/add', promotions.bout_add, name='bout_add'),
        path('events/<int:pk>/bout/<int:bout_pk>/', promotions.BoutView, name='bout'),
        path('events/<int:pk>/bout/<int:bout_pk>/finished/<int:fighter_pk>', promotions.finished_bout, name='finished_bout'),
        path('events/<int:pk>/bout/<int:bout_pk>/finished/draw', promotions.draw_bout, name='draw_bout'),
        path('events/<int:pk>/bout/<int:bout_pk>/finished/nc', promotions.nc_bout, name='nc_bout'),
        path('events/<int:pk>/bout/<int:bout_pk>/offer/<int:fighter_pk>', promotions.offer, name='offer'),
        path('events/<int:pk>/bout/<int:bout_pk>/removefighters', promotions.removeFighters, name='remove_fighters'),
        path('events/<int:pk>/bout/<int:bout_pk>/offerfight', promotions.offer_fight, name='offer_fight'),
    ], 'ammamanager'), namespace='promotions')),
]
