from django.contrib import admin

from an_app.models import Message,Chat,Contact


# Register your models here.
admin.site.register(Message)
admin.site.register(Chat)
admin.site.register(Contact)