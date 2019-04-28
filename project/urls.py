from django.urls import include, path
from django.contrib import admin
from ammamanager.views import ammamanager, gyms, promotions

urlpatterns = [
    path('', include('ammamanager.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/signup/', ammamanager.SignUpView.as_view(), name='signup'),
    path('accounts/signup/gym/', gyms.GymSignUpView.as_view(), name='gym_signup'),
    path('accounts/signup/promotion/', promotions.PromotionSignUpView.as_view(), name='promotion_signup'),
]

