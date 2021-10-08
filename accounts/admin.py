from django.contrib import admin
from .models import Profile, Contact


class ProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "date_of_birth", "photo"]


admin.site.register(Profile, ProfileAdmin)


class ContactAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Contact._meta.get_fields()]


admin.site.register(Contact, ContactAdmin)
