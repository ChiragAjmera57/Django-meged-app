from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/new/', views.post_new, name='post_new'),
    path('login/', views.login_view, name='login'),
    path('logout',views.LogoutInterface.as_view()),
    path('register/', views.register_view, name='register'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('post/cat', views.Cat_list, name='Cat_list'),
    path('post/tag', views.Tag_list, name='Tag_list'),
    path('post/reply/<int:comment_id>',views.reply_to_comment,name='reply_to_comment'),
    path('post/<post_slug>/', views.post_detail, name='post_detail'),
    path('post/<post_slug>/edit/', views.post_edit, name='post_edit'),
    path('cat/<category_slug>',views.Cat_Details,name='Cat_post'),
    path('tag/<tag_slug>',views.Tag_Details,name='Tag_post')
]