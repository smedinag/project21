from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.template import loader
from .models import Question, Choice

# Create your views here.

#def index(request):
#    return HttpResponse("Hola, hoy es septiembre 21 de 2021. Estas en el index de polls!")

#def index(request):
#    latest_question_list = Question.objects.order_by('-pub_date')[:5]
#    output= ','.join([q.question_text for q in latest_question_list])
#    return HttpResponse(output)
##-------------------------
def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]

    #template = loader.get_template('polls/index.html') ## loader es necesario si se usa el HtppResponse
    context= {
        'latest_question_list': latest_question_list,
    }
    #return HttpResponse(template.render(context, request))
    return render(request, 'polls/index.html', context)

#def detail(request, question_id):
#    return HttpResponse('Estás viendo la pregunta # %s.' % question_id)

#def detail(request, question_id):
#   try:
#        question = Question.objects.get(pk=question_id)
#    except Question.DoesNotExist:
#        raise Http404('Esta pregunta no existe!')
#    return render(request, 'polls/detail.html', {'question': question})

def detail(request, question_id):
    question= get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})


def results(request, question_id):
    question= get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except(KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {'question': question, 'error_message': "No seleccionaste una opcion",})
    else:
        selected_choice.votes += 1
        selected_choice.save()
    return HttpResponseRedirect(reverse('polls:results',args=(question.id,)))


    #return HttpResponse('Estás votando en la pregunta %s' % question_id) ## version 1
