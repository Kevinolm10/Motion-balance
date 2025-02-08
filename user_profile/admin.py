from django.contrib import admin
from .models import UserProfile

# Register your models here.
class UserProfileAdmin(admin.ModelAdmin):
    # Display the user, first name, and last name in the admin panel
    list_display = ('user', 'first_name', 'last_name')  

# Register the UserProfile model with the UserProfileAdmin class
admin.site.register(UserProfile, UserProfileAdmin)
