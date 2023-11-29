from django.contrib import admin
from .models import Profile



@admin.register(Profile)
class ProfileUser(admin.ModelAdmin):
    list_display = 'user', 'bio', 'avatar'



