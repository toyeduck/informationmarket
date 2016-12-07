import requests
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from .models import Question, Choice, Bet
from django.shortcuts import get_object_or_404, render
from django import forms
from django.template import loader

def index(request):
	latest_question_list = Question.objects.order_by('-pub_date')[:5]

	template = loader.get_template('infomarket/index.html')
	context = {
	'latest_question_list': latest_question_list,
	}
	return HttpResponse(template.render(context, request))
	#latest_question_list = Question.objects.order_by('-pub_date')[:5]
	#output = ', '.join([q.question_text for q in latest_question_list])
	#return HttpResponse(output)
	#return render(request, 'infomarket/index.html')

def login(request):
	return render(request, 'infomarket/login.html')

def create(request):
	return render(request, 'infomarket/create.html')

# def place(request):
# 	return render(request, 'infomarket/place.html')

def place(request, question_id):
	question = get_object_or_404(Question, pk=question_id)
	try:
		selected_choice = question.choice_set.get(pk=request.POST['choice'])
	except (KeyError, Choice.DoesNotExist):
		# Redisplay the question voting form.
		return render(request, 'infomarket/place.html', {
			'question': question,
			'error_message': "You didn't select a choice.",
		})
	else:
		selected_bet = selected_choice.bet_set.create(bet_user=request.POST['bet_user_name'],bet_amount=10)
		#selected_choice.votes += 1
		selected_bet.save()
		return HttpResponseRedirect(reverse('index', args=(question.id,)))
		# Always return an HttpResponseRedirect after successfully dealing
		# with POST data. This prevents data from being posted twice if a
		# user hits the Back button.
		#return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))