from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'gender', 'phone', 'dob', 'designation', 'address', 'pincode', 'city', 'state', 'country', 'img')

    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': ('username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'is_staff', 'gender', 'phone', 'dob', 'designation', 'address', 'pincode', 'city', 'state', 'country', 'img'),
            }
        ),
    )

    fieldsets = (
        (None, {'fields': ('username', 'email', 'password', 'first_name', 'last_name', 'last_login')}),
        ("Other", {'fields': ('gender', 'phone', 'dob', 'designation', 'address', 'pincode', 'city', 'state', 'country', 'img'), "classes": ("collapse",)}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
