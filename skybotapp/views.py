import json
import requests
from pprint import pprint
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from wit import Wit
from django.views import generic
from django.http.response import HttpResponse
from django.template.context_processors import request
# Create your views here.

def post_facebook_message(fbid, recevied_message):           
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=EAASfh0TDd8cBAHBMfkWQGAexatTOup01lZCXtUJ5CF5Imr5b7MeQu30v6TnEzQmvoJF9MZBzkoZBdhLaVcCSY2BtPivUNJh7pic5vfEA13qDr3TRQLuHn8aKpKZAip4X2QHqhBTa7XQNGPnII1cqNMP46gAaRYMzHHSnZA4NZCAwZDZD' 
    response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"text":recevied_message}})
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
    pprint(status.json())


def send(request, response):
    pprint('Sending to user...', response['text'])
def my_action(request):
    pprint('Received from user...', request['text'])



def witConnect(incoming_message):  
    actions = {
        'send': send,
        'my_action': my_action,
    }  
    client = Wit(access_token='KVCNXSS7SD5RENA5PQ6QBS242ETDIBHC', actions=actions)
    try:
        resp=client.interactive(incoming_message)
        #resp = client.message(incoming_message)
        pprint('Yay, got Wit.ai response: ' + str(resp))
        return resp
    except:
        pprint('WIT.AI ERROR')
    
#KVCNXSS7SD5RENA5PQ6QBS242ETDIBHC
#turgut DJE4HFOBMAJO6DMIC2IEZRP5DDRQRZKS    


class SkyBotView(generic.View):
   # def get(self, request, *args, **kwargs):
    #    if self.request.GET['hub.verify_token'] == '93985762':
     #       return HttpResponse(self.request.GET['hub.challenge'])
      #  else:
       #     return HttpResponse('Error, invalid token')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return generic.View.dispatch(self, request, *args, **kwargs)



    # Post function to handle Facebook messages
    def post(self, request, *args, **kwargs):
        # Converts the text payload into a python dictionary
        incoming_message = json.loads(self.request.body.decode('utf-8'))
        # Facebook recommends going through every entry since they might send
        # multiple messages in a single call during high load
        for entry in incoming_message['entry']:
            for message in entry['messaging']:
                # Check to make sure the received call is a message call
                # This might be delivery, optin, postback for other events 
                if 'message' in message:
                    # Print the message to the terminal

                    pprint(message)
                    resp=witConnect(message['message']['text'])
                    
                    post_facebook_message(message['sender']['id'],str(resp) )     
        return HttpResponse()


#message['message']['text']
#resp['entities']['location'][0]['value']


def homeView(request):
    return HttpResponse('Hello')



#actions = {
#    'send': send,
#    'my_action': my_action,
#}




