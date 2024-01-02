from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, render
from django.shortcuts import render
from django.shortcuts import get_object_or_404, render
from django.http import  HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.contrib.auth.decorators import login_required
from .models import Question
from .models import Choice, Question

class IndexView(generic.ListView,LoginRequiredMixin):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"
    slug_field = 'que_slug'
    slug_url_kwarg = 'que_slug'
    success_url = '/polls'

    def get_queryset(self):
        return Question.objects.order_by("-pub_date")


class DetailView(generic.DetailView,LoginRequiredMixin):
    model = Question
    slug_field = 'que_slug'
    slug_url_kwarg = 'que_slug'
    template_name = "polls/detail.html"
    def get_login_url(self):
        return super().get_login_url() + f'?next={self.request.path}'


class ResultsView(generic.DetailView,LoginRequiredMixin):
    model = Question
    template_name = "polls/results.html"
    slug_field = 'que_slug'
    slug_url_kwarg = 'que_slug'

def vote(request, que_slug):
    question = get_object_or_404(Question, que_slug=que_slug)
    slug_field = 'que_slug'
    slug_url_kwarg = 'que_slug'
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes += 1
        selected_choice.save()
       
        return HttpResponseRedirect(reverse("polls:results", args=(question.que_slug,)))