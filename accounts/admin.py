from django.contrib import admin

# Register your models here.
from .models import UserStripe, EmailConfirmed, EmailSignUpforMarketing

admin.site.register(UserStripe)
admin.site.register(EmailConfirmed)


class EmailMarketingSignUpAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'timestamp']

    class Meta:
        model = EmailSignUpforMarketing


admin.site.register(EmailSignUpforMarketing,EmailMarketingSignUpAdmin)
