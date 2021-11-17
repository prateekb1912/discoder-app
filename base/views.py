from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return HttpResponse('Home Page ANNA')

def room(request):
    return HttpResponse("Room for You")