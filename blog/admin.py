from django.contrib import admin
from .models import Post

class PostAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ['title', 'author', 'published_date', 'post_slug']}),
       
    ]
    list_display = ('title', 'author', 'published_date', 'post_slug')
    search_fields = ['title', 'text',"post_slug"]

admin.site.register(Post, PostAdmin)
