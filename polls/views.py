from django.http import HttpResponse
from .models import Question
from django.shortcuts import get_object_or_404, render
from django.http import Http404
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from .models import Choice, Question

class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"
    slug_field = 'que_slug'
    slug_url_kwarg = 'que_slug'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by("-pub_date")[:5]


class DetailView(generic.DetailView):
    model = Question
    slug_field = 'que_slug'
    slug_url_kwarg = 'que_slug'
    template_name = "polls/detail.html"


class ResultsView(generic.DetailView):
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
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse("polls:results", args=(question.que_slug,)))