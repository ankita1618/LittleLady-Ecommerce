import re
from django.shortcuts import render, HttpResponseRedirect, Http404
from django.contrib.auth import logout, login, authenticate
from .forms import LoginForm, RegistrationForm
from .models import EmailConfirmed
from django.contrib import messages
from django.urls import reverse


# Create your views here.

def logout_view(request):
    logout(request)
    messages.success(request, "Successfully logged out. Feel free to <a href = '%s'> login </a> again." % (reverse("auth_login")),extra_tags='safe')
    # messages.success(request, "Warning.")
    # messages.success(request, "Error")
    return HttpResponseRedirect('%s' % (reverse("auth_login")))  # login


def login_view(request):
    form = LoginForm(request.POST or None)  # if post data then take it otherwise take none
    # checking username and password they exist
    btn = "Login"
    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)
        login(request, user)
        messages.success(request, "Successfully Logged In.")
        return HttpResponseRedirect("/")  # home

    context = {
        "form": form,
        "submit_btn": btn,
    }
    return render(request, "form.html", context)


def registration_view(request):
    form = RegistrationForm(request.POST or None)  # if post data then take it otherwise take none
    # checking username and password they
    btn = "Join"
    if form.is_valid():
        new_user = form.save(commit=False)
        new_user.save()
        messages.success(request, "Successfully Registered. Please confirm your email.")
        return HttpResponseRedirect("/")
        # username = form.cleaned_data['username']
        # password = form.cleaned_data['password']
        # user = authenticate(username=username, password=password)
        # login(request, user)

    context = {
        "form": form,
        "submit_btn": btn,
    }
    return render(request, "form.html", context)


# regular expression
SH1_RE = re.compile('^[a-f0-9]{40}$')


def activation_view(request, activation_key):
    if SH1_RE.search(activation_key):
        print("activation key is real")
        try:  # user_confirmed =instance
            instance = EmailConfirmed.objects.get(activation_key=activation_key)
        except EmailConfirmed.DoesNotExist:
            instance = None
            messages.success(request, "There was an error with your request.")
            return HttpResponseRedirect("/")
        if instance is not None and not instance.confirmed:
            page_message = "Confirmation Successful! Welcome."
            instance.confirmed = True
            instance.activation_key = "Confirmed"
            instance.save()
            messages.success(request, "Successfully Confirmed. Please login")

        elif instance is not None and instance.confirmed:
            page_message = "Already Confirmed"
            messages.success(request, "Already Registered.")

        else:
            page_message = ""
            pass

        context = {
            "page_message": page_message,
        }
        return render(request, "accounts/activation_complete.html", context)
    else:
        raise Http404



