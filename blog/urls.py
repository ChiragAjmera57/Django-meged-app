from django.urls import path
from django.urls import include
from . import views

app_name = "blog"
urlpatterns = [
    path('post/<post_slug>/edit/', views.post_edit, name='post_edit'),
    path('post/new-post/', views.post_new, name='post_new'),
    path('post/<post_slug>/', views.post_detail, name='post_detail'),
    path('user/<str:username>/', views.user_detail, name='user_detail'),
    path('tag/<tag_slug>',views.tag_details,name='Tag_post'),
    path('cat/<category_slug>',views.cat_details,name='Cat_post'),
    path('post/cat', views.cat_list, name='Cat_list'),
    path('post/tag', views.tag_list, name='Tag_list'),
    path('comment/reply/', views.reply_page, name="reply"),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
     path('bulk_post_upload/',views.bulk_post_upload, name='bulk_post_upload'),
    path('', views.post_list, name='post_list'),
]