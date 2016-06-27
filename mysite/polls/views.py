from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from .models import Question, Choice
from django.db.models import F


def index(request):
    """Renders the home page of the polls app."""

    # get the most recent 5 questions from the db
    latest_question_list = Question.objects.order_by('-pub_date')[:5]

    # load the index template from polls/templates/polls/
    template = loader.get_template('polls/index.html')

    # set up context as dictionary with variables to pass to render view
    context = {
        'latest_question_list': latest_question_list,
    }

    # render the template with the context as a response to the request
    return HttpResponse(template.render(context, request))

    # can also use (negates the need for 'loader' and 'HttpResponse' objects):
    # return render(request, 'polls/index.html', context)


def detail(request, question_id):
    """View the details of a question"""

    # make sure question exists
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")

    # return rendered template for question's detail view
    return render(request, 'polls/detail.html', {'question': question})

    # could also use get() and riase Http404:

    # question = get_object_or_404(Question, pk=question_id)
    # return render(request, 'polls/detail.html', {'question': question})


def results(request, question_id):
    """Displays the results of the poll after voting"""

    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})


def vote(request, question_id):
    """Handles submitting a vote. Redirects to results view"""

    # get Question object from db
    question = get_object_or_404(Question, pk=question_id)

    # get choice voted for (request.CHOICE['choice'] returns str of choice ID)
    # or insist the user votes again with error msg
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # redisplay the question voting form (details view)
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice."
        })
    # increment votes for choice. Use of F() allows simultaneous voting
    # redirects to results view
    else:
        selected_choice.update(votes = F('votes') + 1)
        return HttpResponseRedirect(
            reverse('polls:results', args=(question.id,))
        )

