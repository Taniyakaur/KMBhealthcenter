from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, "hello/index.html")

def taniya(request):
    return HttpResponse("Hello Taniya!")

def greet(request, name):
    return HttpResponse(f"Hello, {name.capitalize()}!")
