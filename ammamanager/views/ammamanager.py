from django.shortcuts import redirect, render
from django.views.generic import TemplateView


class SignUpView(TemplateView):
    template_name = 'registration/signup.html'


def index(request):
    return render(request, 'index.html')


def home(request):
    if request.user.is_authenticated:
        if request.user.is_promotion:
            return redirect('promotions:promotion_home')
        else:
            return redirect('gyms:gym_home')
    return render(request, 'ammamanager/home.html')
