from django.contrib import admin
from .models import UserProfile


"""Admin interface for UserProfile model."""
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name')


admin.site.register(UserProfile, UserProfileAdmin)
