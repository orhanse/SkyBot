from django.shortcuts import render
# yomamabot/fb_yomamabot/views.py
from django.views import generic
from django.http.response import HttpResponse
# Create your views here.
class SkyBotView(generic.View):
    def get(self, request, *args, **kwargs):
        return HttpResponse("Hello World!")
