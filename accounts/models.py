from django.core.mail import send_mail
from django.db import models
from django.conf import settings
from django.template.loader import render_to_string
from django.urls import reverse


# Create your models here.


# creating stripe account #signal send saying a msg if user login and that will run a function
class UserStripe(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    stripe_id = models.CharField(max_length=120, null=True, blank=True)

    def __str__(self):
        return str(self.stripe_id)


class EmailConfirmed(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    activation_key = models.CharField(max_length=200)
    confirmed = models.BooleanField(default=False)

    def __str__(self):
        return str(self.confirmed)

    def activate_user_email(self):
        # send email here and render a string
        activation_url = "%s%s" % (settings.SITE_URL, reverse("activation_view", args=[self.activation_key]))
        context = {
            "activation_key": self.activation_key,
            "activation_url": activation_url,
            "user": self.user.username,
        }
        message = render_to_string("accounts/activation_message.txt", context)
        subject = "Activate your Email"
        self.email_user(subject, message, settings.DEFAULT_FROM_EMAIL)

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.user.email], **kwargs)


class EmailSignUpforMarketing(models.Model):
    email = models.EmailField()
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    update = models.DateTimeField(auto_now_add=False, auto_now=True)
# at some point we can add confirmed to confirm the email

    def __str__(self):
        return str(self.email)
