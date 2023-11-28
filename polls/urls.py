from django.urls import path

from . import views

app_name = "polls"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("<que_slug>/", views.DetailView.as_view(), name="detail"),
    path("<que_slug>/results/", views.ResultsView.as_view(), name="results"),
    path("<que_slug>/vote/", views.vote, name="vote"),
]