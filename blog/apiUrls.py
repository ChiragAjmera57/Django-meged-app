from django.urls import include, path
from rest_framework.authtoken import views
from rest_framework import routers

from blog.apiViews import *

router = routers.DefaultRouter()
router.register('users', UserViewSet)
router.register('posts', PostViewSet)
router.register('category', CategoryViewSet)
router.register('tags', TagViewSet)
router.register('comment', CommentViewSet)
router.register('login', LoginViewSet ,basename="logined")
router.register('signup', UserSignViewSet ,basename="signup")



urlpatterns = [
    path('api-token-auth/', views.obtain_auth_token),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('', include(router.urls)),
    path('user-profile/', UserProfileView.as_view(), name='user-profile'),

    
]
