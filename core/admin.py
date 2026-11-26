from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, FoodListing, ContactMessage

admin.site.register(User, UserAdmin)
admin.site.register(FoodListing)
admin.site.register(ContactMessage)