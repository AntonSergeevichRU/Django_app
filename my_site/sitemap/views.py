from django.http import HttpResponse
from django.shortcuts import render



def info(request):
    return HttpResponse("<h2>Что то тут есть</h2>")
