from django.urls import path
from django.contrib.auth.decorators import login_required


from . import views

app_name = "polls"
urlpatterns = [
    path("<que_slug>/results/", views.ResultsView.as_view(), name="results"),
    path("<que_slug>/vote/", views.vote, name="vote"),
    path("<que_slug>/", views.DetailView.as_view(), name="detail"),
    path("", views.IndexView.as_view(login_url='/login'), name="index"),
]