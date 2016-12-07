import requests
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from .models import Question, Choice, Bet
from django.shortcuts import get_object_or_404, render
from django import forms
from django.template import loader
from django.utils import timezone

def index(request):
	#Update total bets
	question_list = Question.objects.all()
	for question in question_list:
		choice_list = question.choice_set.all()
		for choice in choice_list:
			total_choice_bet = 0
			bet_list = choice.bet_set.all()
			for bet in bet_list:
				total_choice_bet += bet.bet_amount
			choice.total_bet = total_choice_bet
			choice.save()

	#Calculate chance to win
	updated_question_list = Question.objects.all()
	for question in updated_question_list:
		choice_list = question.choice_set.all()
		total_bet = 0.0
		for choice in choice_list:
			total_bet += choice.total_bet
		#print(total_bet)
		if total_bet != 0.0:
			for choice in choice_list:
				choice.chance_to_win = int(choice.total_bet*100/total_bet)
				choice.save()

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
	try:
		new_question = Question(question_text=request.POST['question'], pub_date=timezone.now(), pub_user=request.POST['name'])
	except (KeyError, Choice.DoesNotExist):
		# Redisplay the question creating form.
		return render(request, 'infomarket/create.html', {
			#'question': question,
			'error_message': "You didn't input a question.",
		})
	else:
		new_question.save()
		new_bet_1 = new_question.choice_set.create(choice_text=request.POST['outcome-a'],total_bet=0)
		new_bet_1.save()
		new_bet_2 = new_question.choice_set.create(choice_text=request.POST['outcome-b'],total_bet=0)
		new_bet_2.save()
		#return HttpResponseRedirect(reverse('index', args=(question.id,)))
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
		return HttpResponseRedirect(reverse('place', args=(question.id,)))
		#return HttpResponseRedirect(reverse('index', args=(question.id,)))
		# Always return an HttpResponseRedirect after successfully dealing
		# with POST data. This prevents data from being posted twice if a
		# user hits the Back button.
		#return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))