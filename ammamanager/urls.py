from django.urls import include, path

from .views import ammamanager, gyms, promotions

urlpatterns = [
    path('', ammamanager.home, name='home'),

    path('gyms/', include(([
        path('', gyms.QuizListView.as_view(), name='quiz_list'),
        path('fighters/', gyms.ListFightersView.as_view(), name='fighter_list'),
        path('fighters/add/', gyms.FighterCreateView.as_view(), name='fighter_add'),
    ], 'ammamanager'), namespace='gyms')),





    path('promotions/', include(([
        path('', promotions.QuizListView.as_view(), name='quiz_change_list'),
    ], 'ammamanager'), namespace='promotions')),
]
