from django.shortcuts import render
# yomamabot/fb_yomamabot/views.py
from django.views import generic
from django.http.response import HttpResponse
# Create your views here.
class SkyBotView(generic.View):
    def get(self, request, *args, **kwargs):
        if self.request.GET.get['hub.verify_token'] == '20170421':
            return HttpResponse(self.request.GET.get['hub.challenge'])
        else:
            return HttpResponse('Error, invalid token')
      

#@method_decorator(csrf_exempt)
#def dispatch(self, request, *args, **kwargs):
#    return generic.View.dispatch(self, request, *args, **kwargs)
