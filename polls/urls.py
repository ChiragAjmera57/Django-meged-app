from django.urls import path
from django.contrib.auth.decorators import login_required


from . import views

app_name = "polls"
urlpatterns = [
    path("", views.IndexView.as_view(login_url='/login'), name="index"),
    path("<que_slug>/", login_required(views.DetailView.as_view(login_url='/login')), name="detail"),
    path("<que_slug>/results/", login_required(views.ResultsView.as_view(login_url='/login')), name="results"),
    path("<que_slug>/vote/", views.vote, name="vote"),
]