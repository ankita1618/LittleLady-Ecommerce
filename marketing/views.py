import json
import datetime

from django.http import HttpResponseBadRequest
from django.shortcuts import render, HttpResponse, Http404
from django.utils import timezone
from django.conf import settings
from .forms import EmailForm
from accounts.models import EmailSignUpforMarketing

# Create your views here.

def dismiss_marketing_msg(request):
    if request.is_ajax():
        data = {"success": True}
        json_data = json.dumps(data)
        request.session['dismiss_message_for'] = str(
            timezone.now() + datetime.timedelta(hours=settings.MARKETING_HOUR_OFFSET,
                                                seconds=settings.MARKETING_SECOND_OFFSET))
        return HttpResponse(json_data, content_type='application/json')
    else:
        raise Http404


def email_signup(request):
    if request.method == "POST":
        # print(request.POST)
        form = EmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            new_signup = EmailSignUpforMarketing.objects.create(email=email)
            request.session['email_added_marketing'] = True
            return HttpResponse('Success %s' % (email))
        if form.errors:
            # print(form.errors)
            json_data = json.dumps(form.errors)
            return HttpResponseBadRequest(json_data, content_type='application/json')
    else:
        raise Http404
