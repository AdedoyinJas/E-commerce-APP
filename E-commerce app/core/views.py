from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return HttpResponse('<h1> WELCOME TO THE E-COMMERCE APP </h1>')

# Create your views here.
