from django.http import HttpResponse
from django.shortcuts import render



def test(request,**kwargs):
    print("test")
    return HttpResponse("test")