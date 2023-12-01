from django.contrib import admin
from .models import Category, Post, Tag

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

# class CategoryInline(admin.TabularInline):  # or use admin.StackedInline for a stacked display
#     model = Category
#     extra = 1  # Number of empty forms to show

# class PostAdmin(admin.ModelAdmin):
#     inlines = [CategoryInline]
#     list_display = ('title', 'author', 'published_date')  # Add other fields you want to display in the list

# admin.site.register(Post, PostAdmin)
# admin.site.register(Category)
admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Tag)


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
