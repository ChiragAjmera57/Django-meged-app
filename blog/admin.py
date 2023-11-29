from django.contrib import admin
from .models import Category, Post, Tag

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