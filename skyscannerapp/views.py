from django.http import HttpResponse
import requests, json

def flight(request):
    
    result=json.loads(json.dumps({'price': 0, 'out': {'date': '', 'place':'', 'carrier':''}, 'in':{'date': '', 'place':'', 'carrier':''}})) # direct???
    origin=id_finder('istanbul')
    destination=id_finder('madrid')
    outbounddate='2017-06-10'
    inbounddate='2017-06-15'
    
    if (origin==None or destination==None) or len(outbounddate) != len(inbounddate) and len(inbounddate)!=0:   # lokasyon, date kontrolu 
        result=None
        HttpResponse(result)
    query=requests.get('http://partners.api.skyscanner.net/apiservices/browsequotes/v1.0/tr/try/tr/'+origin+'/'+destination+'/'+outbounddate+'/'+inbounddate+'?apiKey=sk183163813532396485407386558735') 
    data=query.json()
    if len(data['Quotes'])==0:  # Bu parametrelere uyan bir ucus yok.
        result=None
        HttpResponse(result)
    if 'Inbound' in data['Quotes'][0]:
        roundtrip=True
    else:
        roundtrip=False
    result['price']=data['Quotes'][0]['MinPrice']
    result['out']['date']=data['Quotes'][0]['OutboundLeg']['DepartureDate']
    if roundtrip == True:
        result['in']['date'] = data['Quotes'][0]['InboundLeg']['DepartureDate']
    
    for i in range(0, len(data['Places'])):   # DEPARTURE AIRPORTS
        if data['Places'][i]['Type'] == 'Station' and data['Places'][i]['PlaceId'] == data['Quotes'][0]['OutboundLeg']['OriginId']:
            result['out']['place'] = data['Places'][i]['Name']
             
    for i in range(0, len(data['Places'])):
        if roundtrip == True and data['Places'][i]['Type'] == 'Station' and data['Places'][i]['PlaceId'] == data['Quotes'][0]['InboundLeg']['OriginId']:
            result['in']['place'] = data['Places'][i]['Name']
            
    for i in range(0, len(data['Carriers'])):     # CARRIER NAMES
        if data['Carriers'][i]['CarrierId'] == data['Quotes'][0]['OutboundLeg']['CarrierIds'][0]:
            result['out']['carrier'] = data['Carriers'][i]['Name']
            
    for i in range(0, len(data['Carriers'])):     # CARRIER NAMES
        if roundtrip==True and data['Carriers'][i]['CarrierId']==data['Quotes'][0]['InboundLeg']['CarrierIds'][0]:
            result['in']['carrier'] = data['Carriers'][i]['Name']
            
    return HttpResponse(str(result))