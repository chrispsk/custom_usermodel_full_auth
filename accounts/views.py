from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from .forms import UserCreationForm, UserLoginForm
from django.contrib.auth import login, get_user_model, logout
from .models import ActivationKey


User = get_user_model()
def home(request):
    if request.user.is_authenticated:
        print(request.user.profile.city)
    return HttpResponse("ok")

def register(request):

    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        # FOR NO EXTENSION
        user = form.save() # Save in database
        # FOR EXTENSION
        user.profile.city = form.cleaned_data.get('city')
        user.save()

        return HttpResponseRedirect("/accounts/login")
    return render(request,'registration.html', {'user_form':form})

def user_login(request):
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        email = form.cleaned_data.get('email')
        user_obj = User.objects.get(email__iexact=email)
        login(request, user_obj)
        return HttpResponseRedirect("/")
    return render(request,'login.html', {'user_form':form})

def user_logout(request):
    logout(request)
    return HttpResponseRedirect("/accounts/login")

def activate_user(request, code=None):
    if code:
        act_profile = ActivationKey.objects.filter(key=code)
        if act_profile.exists() and act_profile.count() == 1:
            act_obj = act_profile.first()
            if not act_obj.expired:
                user_obj = act_obj.user
                user_obj.is_active = True
                user_obj.save()
                user_obj.expired = False
                user_obj.save()
                return HttpResponseRedirect("/accounts/login")
    # invalid code
    return HttpResponseRedirect("/accounts/login")
