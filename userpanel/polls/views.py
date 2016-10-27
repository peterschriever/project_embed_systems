from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from polls.models import Question
# from django.template import loader

# Create your views here.
def index(request):
    # retrieve data
    latestQuestionList = Question.objects.order_by('-date_published')[:5]

    # define data for use in view context
    viewContext = {
        'latestQuestionList': latestQuestionList,
    }

    # render view with template /polls/templates/polls/index.html
    return render(request, 'polls/index.html', viewContext)

def detail(request, questionId):
    question = get_object_or_404(Question, pk=questionId)
    return render(request, 'polls/detail.html', {'question': question})

def results(request, questionId):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % questionId)

def vote(request, questionId):
    return HttpResponse("You're voting on question %s." % questionId)
