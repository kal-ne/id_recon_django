from django.shortcuts import render
from django.http import HttpResponse

def identity(request):
    return HttpResponse("Hello, world. This is the id api!")