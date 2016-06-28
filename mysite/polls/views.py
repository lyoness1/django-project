from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from django.db.models import F

from .models import Question, Choice


class IndexView(generic.ListView):
    """Displays generic view of index.html with question list"""

    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    """Handles submitting a vote. Redirects to results view"""

    # get Question object from db
    question = get_object_or_404(Question, pk=question_id)

    # get choice voted for (request.CHOICE['choice'] returns str of choice ID)
    # or insist the user votes again with error msg
    try:
        selected_choice = question.choice_set.filter(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # redisplay the question voting form (details view)
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice."
        })
    else:
        selected_choice.update(votes=F('votes') + 1)
        return HttpResponseRedirect(
            reverse('polls:results', args=(question.id,))
        )