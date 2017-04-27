from django.http import HttpResponse
import requests, json, datetime

def flight(list):
    
	if list[4] == None:
		inbounddate=''
		roundTrip = True
	else:
		inbounddate=str(list[4])[:10]
		roundTrip = False
		
	if list[3] == None:
		list[3] = str(datetime.date.today())
        
    result = json.loads(json.dumps({'price': 0, 'out': {'date': '', 'from':'', 'to':'', 'carrier':''}, 'in':{'date': '', 'from':'','to':'','carrier':''}})) # direct???
    origin=id_finder(list[0])
    destination=id_finder(list[1])
    outbounddate=list[3][:10]
	
	if origin == None or destination == None:
		return 'Yanlis konum bilgisi'
    
    if len(outbounddate) != len(inbounddate) and len(inbounddate)!=0:   # date kontrolu 
        return 'Girilen tarihler uyumsuz'
 
    query=requests.get('http://partners.api.skyscanner.net/apiservices/browsequotes/v1.0/tr/try/tr/'+origin+'/'+destination+'/'+outbounddate+'/'+inbounddate+'?apiKey=sk183163813532396485407386558735') 
    data=query.json()
	
    if len(data['Quotes'])==0:  # Bu parametrelere uyan bir ucus yok.
        return 'Parametrelere uygun sonuc bulunamadi'
        
    for i in range(0, len(data['Quotes'])):
		if (roundTrip and 'InboundLeg' in data['Quotes'][i]) or (not roundtrip and not 'InboundLeg' in data['Quotes'][i]):
		
			result['price']=data['Quotes'][i]['MinPrice']
			result['out']['date']=str(data['Quotes'][i]['OutboundLeg']['DepartureDate'])[:10]
			result['direct'] = data['Quotes'][i]['Direct']
			if roundtrip == True:
				result['in']['date'] = str(data['Quotes'][i]['InboundLeg']['DepartureDate'])[:10]
			for j in range(0, len('Places')):
			
				if data['Places'][j]['Type'] == 'Station' and data['Places'][j]['PlaceId'] == data['Quotes'][i]['OutboundLeg']['OriginId']:
					result['out']['from'] = data['Places'][j]['Name']
				if data['Places'][j]['Type'] == 'Station' and data['Places'][j]['PlaceId'] == data['Quotes'][i]['OutboundLeg']['DestinationId']:
					result['out']['to'] = data['Places'][j]['Name']
				if roundtrip == True and data['Places'][j]['Type'] == 'Station' and data['Places'][j]['PlaceId'] == data['Quotes'][i]['InboundLeg']['OriginId']:
					result['in']['from'] = data['Places'][j]['Name']
				if roundtrip == True and data['Places'][j]['Type'] == 'Station' and data['Places'][j]['PlaceId'] == data['Quotes'][i]['InboundLeg']['DestinationId']:
					result['in']['to'] = data['Places'][j]['Name']
					
			for j in range(0, len(data['Carriers'])):     # CARRIER NAMES
				if data['Carriers'][j]['CarrierId'] == data['Quotes'][i]['OutboundLeg']['CarrierIds'][0]:
					result['out']['carrier'] = data['Carriers'][j]['Name']
            
				if roundtrip==True and data['Carriers'][j]['CarrierId']==data['Quotes'][i]['InboundLeg']['CarrierIds'][0]:
					result['in']['carrier'] = data['Carriers'][j]['Name']
            
    return result

def id_finder(place):
    result=requests.get('http://partners.api.skyscanner.net/apiservices/autosuggest/v1.0/tr/TRY/en-US?query='+place+'&apiKey=sk183163813532396485407386558735')
    record=result.json()
    if(len(record['Places'])==0): # boyle bir yer var mi?
        return None
    name=record['Places'][0]['PlaceId']
    return str(name)