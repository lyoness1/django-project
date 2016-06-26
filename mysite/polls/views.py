from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from .models import Question


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
    return HttpResponse("You're looking at question %s." % question_id)

def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)

def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)
