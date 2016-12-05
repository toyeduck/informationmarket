from django.shortcuts import render
import requests

def index(request):
	 return render(request, 'infomarket/index.html')

def login(request):
	 return render(request, 'infomarket/login.html')

def create(request):
	 return render(request, 'infomarket/create.html')

def place(request):
	 return render(request, 'infomarket/place.html')