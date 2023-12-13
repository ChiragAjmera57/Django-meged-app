from django.urls import reverse
from django.contrib import admin
from django.http import HttpResponse
from django.contrib.auth.admin import UserAdmin
import csv

from .models import *
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    actions = ['export_as_csv']

    def export_as_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="users.csv"'

        writer = csv.writer(response)
        writer.writerow([
             'Username', 
             'Email', 
             'First Name', 
             'Last Name', 
             'Gender', 
             'Phone', 
             'Date of Birth', 
             'Designation', 
             'Address', 
             'Pincode', 
             'City', 
             'State', 
             'Country'
             ]
            )

        for user in queryset:
            writer.writerow([
                user.username,
                user.email,
                user.first_name,
                user.last_name,
                user.gender,
                user.phone,
                user.dob,
                user.designation,
                user.address,
                user.pincode,
                user.city,
                user.state,
                user.country,
            ])

        return response

    export_as_csv.short_description = "Export selected users as CSV"
        
    list_display = (
        'username', 
        'email', 
        'first_name', 
        'last_name', 
        'is_staff', 
        'gender', 
        'phone', 
        'dob', 
        'designation', 
        'address', 
        'pincode', 
        'city', 
        'state', 
        'country', 
        'img'
        )

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
        (None, {'fields': ('username', 'email', 'password', 'first_name', 'last_name', 'last_login','is_staff')}),
        ("Other", {'fields': ('gender', 'phone', 'dob', 'designation', 'address', 'pincode', 'city', 'state', 'country', 'img'), "classes": ("collapse",)}),
    )


class CustomPostAdmin(admin.ModelAdmin):
    model = Post
    list_display = ('title','post_cat','img_preview')
    list_filter = ["tags", "published_date","post_cat"]
    filter_horizontal = ('tags',)
    search_fields = ('title',)
    def view_on_site(self, obj):
        url = reverse("blog:post_detail", kwargs={"post_slug": obj.post_slug})
        return url
   
    
class customCatAdmin(admin.ModelAdmin):
    model = Category
    list_filter = ['title','description']
    search_fields = ('title',)
    def has_delete_permission(self, request, obj=None):
        return False
    
    
class CustomCommentAdmin(admin.ModelAdmin):
    model = Comment
    list_display = ['name','post','text','body']
    search_fields = ('text',)
    list_filter = ["created"]
   
    
class CustomtagAdmin(admin.ModelAdmin):
    model = Tag
    search_fields = ('name',)
    list_filter = ['name','description']
    def has_delete_permission(self, request, obj=None):
        return False

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Post,CustomPostAdmin)
admin.site.register(Category,customCatAdmin)
admin.site.register(Comment,CustomCommentAdmin)
admin.site.register(Tag,CustomtagAdmin)