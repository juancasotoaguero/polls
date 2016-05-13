from django.shortcuts import render, get_object_or_404
#from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from polls.models import Question,Choice
#from django.template import loader#utilizamos esa libreria para cargar a parte el template y utilizar HttpResponse


#def index(request):
#    latest_question_list = Question.objects.order_by('-pub_date')[:5]
#    #    template = loader.get_template('polls/index.html')
#    #    context = {
#    #               'latest_question_list':latest_question_list
#    #               }
    
#    return render(request, 'polls/index.html', {'latest_question_list':latest_question_list})#al utilizar render ya no es necesario usar loader ni httpResponse
    #return HttpResponse(template.render(context, request))

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]

#def detail(request, question_id):
##    try:
##        question = Question.objects.get(pk=question_id)
##    except Question.DoesNotExist:
##        raise Http404('Pregunta no existente.')
#    question = get_object_or_404(Question, pk=question_id)#con esto reducimos capas en el view
#    return render(request,'polls/detail.html', { 'pregunta':question})

class DetailView(generic.DetailView):
    model = Question 
    template_name = 'polls/detail.html'


#def results(request, question_id):
#    question = get_object_or_404(Question, pk=question_id)
#    return render(request, 'polls/results.html',{'pregunta':question})

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'
    
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "No seleccionaste ninguna opcion",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results',args=(question.id,)))