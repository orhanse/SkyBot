import json
import requests
from pprint import pprint
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from wit import Wit
from .models import botDB
from django.views import generic
from django.http.response import HttpResponse
from django.template.context_processors import request
import copy, datetime



def post_facebook_message(fbid, recevied_message):           
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=EAASfh0TDd8cBAHBMfkWQGAexatTOup01lZCXtUJ5CF5Imr5b7MeQu30v6TnEzQmvoJF9MZBzkoZBdhLaVcCSY2BtPivUNJh7pic5vfEA13qDr3TRQLuHn8aKpKZAip4X2QHqhBTa7XQNGPnII1cqNMP46gAaRYMzHHSnZA4NZCAwZDZD' 
    response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"text":recevied_message}})
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
    pprint(status.json())


def send(request, response):
    text = str(response['text'])
    text = text[:-1]
    text = text[2:]
    post_facebook_message(request['session_id'],text)     

def receiveAction(request):
    pprint('RECEIVED FROM USER',request['text'])



actions = {'send':send,
           'receiveAction':receiveAction
           }      

client = Wit(access_token='KVCNXSS7SD5RENA5PQ6QBS242ETDIBHC', actions=actions)




def witConnect(incoming_message,userID):  
    try:
        resp = client.message(incoming_message)
        pprint('Yay, got Wit.ai response: ' + str(resp))
        if 'reset' in resp['entities']:
            try:
                 lastMessage = botDB.objects.get(userId = userID)
                 botDB.objects.get(userId = userID).delete()
            except botDB.DoesNotExist:
                 lastMessage = None
       
        return resp
    except:
        pprint('WIT.AI ERROR')
    
 


class SkyBotView(generic.View):
    def get(self, request, *args, **kwargs):
        if self.request.GET['hub.verify_token'] == '93985762':
           return HttpResponse(self.request.GET['hub.challenge'])
        else:
            return HttpResponse('Error, invalid token')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return generic.View.dispatch(self, request, *args, **kwargs)


    def post(self, request, *args, **kwargs):
        incoming_message = json.loads(self.request.body.decode('utf-8'))
        for entry in incoming_message['entry']:
            for message in entry['messaging']: 
                if 'message' in message:
               
                    if message['sender']['id'] != '1884352301811482':
                
                            pprint('THE MESSAGE POSTED TO WITCONNECT FUNCTION : ' + str(message))
                            resp=witConnect(message['message']['text'],message['sender']['id'])
                            strResp = parseWitData(resp,message['sender']['id'])
                            array = ['j','j','j','j']
                            try:
                                lastMessage = botDB.objects.get(userId = message['sender']['id'])
                                if lastMessage.firstLocation != None:
                                    array[0] = lastMessage.firstLocation
                                if lastMessage.secondLocation != None:
                                    array[1] = lastMessage.secondLocation
                                if lastMessage.firstDate != None:
                                    array[2] = lastMessage.firstDate
                                if lastMessage.secondDate != None:
                                    array[3] = lastMessage.secondDate
                            except botDB.DoesNotExist:
                                lastMessage = None
                            check = checkArray(array)
                            pprint('array: ' + str(array))
                            pprint('check: ' + str(check))
                            if check == 1 or 'greeting' in resp['entities'] or 'bye' in resp['entities'] or 'reset' in resp['entities']:
                                client.run_actions(message['sender']['id'], message['message']['text'])
                            else:
                                #if strResp == 'done':
                                 #   botDB.objects.get(userId = message['sender']['id']).delete()
                                  #  post_facebook_message(message['sender']['id'],str(array))
                                #else:
                                post_facebook_message(message['sender']['id'],str(strResp))

                                 
        return HttpResponse()



    
def parseWitData(witOut,senderID):
        array = ['j','j','j','j']
        try:
            lastMessage = botDB.objects.get(userId = senderID)
            if lastMessage.firstLocation != None:
                array[0] = lastMessage.firstLocation
            if lastMessage.secondLocation != None:
                array[1] = lastMessage.secondLocation
            if lastMessage.firstDate != None:
                array[2] = lastMessage.firstDate
            if lastMessage.secondDate != None:
                array[3] = lastMessage.secondDate
        except botDB.DoesNotExist:
            lastMessage = None
            
        pprint('FONKSYONUN BASI: ' + str(array))
        lent = 0
        if 'location' in witOut['entities']:
            lent = len(witOut['entities']['location'])
            if array[0] == 'j':
                if lent == 2:
                   array[0] = str(witOut['entities']['location'][0]['value'])
                   array[1] = str(witOut['entities']['location'][1]['value'])
                elif lent ==1:
                   array[0] = str(witOut['entities']['location'][0]['value'])
            elif array[1] == 'j':
                array[1] = str(witOut['entities']['location'][0]['value'])
        if 'datetime' in witOut['entities']:
            lent = len(witOut['entities']['datetime'][0]['values'])
            if lent > 1:
                if 'to' in  witOut['entities']['datetime'][0]['values'][0]:
                    array[2] = str(witOut['entities']['datetime'][0]['values'][0]['to']['value'])
                    array[3] = str(witOut['entities']['datetime'][0]['values'][0]['from']['value'])
                else:
                    array[2] = str(witOut['entities']['datetime'][0]['values'][0]['value'])  
            else:
                array[2] = str(witOut['entities']['datetime'][0]['values'][0]['value'])
        try:
            botDB.objects.get(userId = senderID).delete()
        except botDB.DoesNotExist:
            pprint('no record')
        newMessage = botDB(userId = senderID,firstLocation=array[0],secondLocation=array[1],firstDate=array[2],secondDate=array[3])
        newMessage.save()
        if array[0] == 'j' :
            pprint(str(array))
            return 'Please enter the destination and source'
        if array[1] =='j':
            pprint(str(array))
            return 'Please enter the destination'
        if array[2] == 'j':
            pprint(str(array))
            return 'Please enter the time you want to fly'
        pprint(str(array))
        return flight(array)
        #return 'done'
    
                    
                 
def checkArray(array):
    flag = 1
    for i in range(0,4):
        if array[i] != 'j':
            flag = 0
    return flag



def homeView(request):
    return HttpResponse('Hello')

def flight(list):
    pprint('CHEAPEST')
    #pprint('query = ' + str(query))
    
    result = json.loads(json.dumps({'price': 0, 'out': {'date': '', 'from': '', 'to': '', 'carrier': ''}, 'in': {'date': '', 'from':'', 'to': '', 'carrier':''}}))
    
    origin = id_finder(query[0])
    destination = id_finder(query[1])
    
    if query[3] == 'j': # tek yon ise
        outbounddate = str(query[2])[:10]
        inbounddate = ''
        roundTrip = False
    else:   # cift yon ise    # tarihlerin yerleri degistirildi
        outbounddate = str(query[3])[:10]
        inbounddate = str(query[2])[:10]
        roundTrip = True
    
    
    pprint('Kontrol 1 = ' + origin + ' ' + destination + ' ' + outbounddate + ' ' + inbounddate)
    
    query=requests.get('http://partners.api.skyscanner.net/apiservices/browsequotes/v1.0/tr/try/tr/'+origin+'/'+destination+'/'+outbounddate+'/'+inbounddate+'?apiKey=sk183163813532396485407386558735') 
    data=query.json()
    
    pprint(str(data))
    if len(data['Quotes']) == 0:
        pprint('ERROR 1 = ' + str(data))
        return 'Bu parametrelere uygun ucus yok'
    
    for i in range(0, len(data['Quotes'])):
        if (roundTrip  and 'InboundLeg' in data['Quotes'][i]) or (not roundTrip  and (not 'InboundLeg' in data['Quotes'][i])):
            pprint('Kontrol 2 = ' + str(data['Quotes'][i]['QuoteId']))
            
            result['price']=data['Quotes'][i]['MinPrice']
            result['out']['date']=str(data['Quotes'][i]['OutboundLeg']['DepartureDate'])[:10]
            
            if roundTrip:
                result['in']['date'] = str(data['Quotes'][i]['InboundLeg']['DepartureDate'])[:10]
            pprint('Kontrol 3 = ' + str(result))
            
            for j in range(0, len(data['Places'])):
                if data['Places'][j]['Type'] == 'Station' and data['Places'][j]['PlaceId'] == data['Quotes'][i]['OutboundLeg']['OriginId']:
                    result['out']['from'] = data['Places'][j]['Name']
                if data['Places'][j]['Type'] == 'Station' and data['Places'][j]['PlaceId'] == data['Quotes'][i]['OutboundLeg']['DestinationId']:
                    result['out']['to'] = data['Places'][j]['Name']
                if roundTrip == True and data['Places'][j]['Type'] == 'Station' and data['Places'][j]['PlaceId'] == data['Quotes'][i]['InboundLeg']['OriginId']:
                    result['in']['from'] = data['Places'][j]['Name']
                if roundTrip == True and data['Places'][j]['Type'] == 'Station' and data['Places'][j]['PlaceId'] == data['Quotes'][i]['InboundLeg']['DestinationId']:
                    result['in']['to'] = data['Places'][j]['Name']
            
            for j in range(0, len(data['Carriers'])):     # CARRIER NAMES
                if data['Carriers'][j]['CarrierId'] == data['Quotes'][i]['OutboundLeg']['CarrierIds'][0]:
                    result['out']['carrier'] = data['Carriers'][j]['Name']
            
                if roundTrip==True and data['Carriers'][j]['CarrierId']==data['Quotes'][i]['InboundLeg']['CarrierIds'][0]:
                    result['in']['carrier'] = data['Carriers'][j]['Name']
            break
        
    pprint('Kontrol 4 = ' + str(result))
    
    if roundTrip:
        printOut = 'The cheapest flight according to informaiton you gave: from ' + result['out']['from'] + ' to ' + result['out']['to'] + ' on ' + result['out']['date'] + ' with ' + result['out']['carrier'] + ' and return is on ' + result['in']['date'] + ' with ' + result['in']['carrier'] + ' for ' + str(result['price']) + ' tl'
    else:
        printOut = 'The cheapest flight according to informaiton you gave: from ' + result['out']['from'] + ' to ' + result['out']['to'] + ' on ' + result['out']['date'] + ' with ' + result['out']['carrier'] + ' for ' + str(result['price']) + ' tl'
    return str(printOut)

def id_finder(place):
    result=requests.get('http://partners.api.skyscanner.net/apiservices/autosuggest/v1.0/tr/TRY/en-US?query='+place+'&apiKey=sk183163813532396485407386558735')
    record=result.json()
    if(len(record['Places'])==0): # boyle bir yer var mi?
        return None
    name=record['Places'][0]['PlaceId']
    return str(name)














