from django.shortcuts import render
from django.http import HttpResponse
from .models import Question

# Create your views here.

#def index(request):
#    return HttpResponse("Hola, hoy es septiembre 21 de 2021. Estas en el index de polls!")

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    output= ','.join([q.question_text for q in latest_question_list])
    return HttpResponse(output)

##-------------------------
def detail(request, question_id):
    return HttpResponse('Estás viendo la pregunta # %s.' % question_id)

def results(request, question_id):
    response= 'Estás viendo los resultados de la pregunta # %s'
    return HttpResponse(response % question_id)

def vote(request, question_id):
    return HttpResponse('Estás votando en la pregunta %s' % question_id)
