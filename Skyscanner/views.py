import json
import requests
import pprint
from django.views import generic
from django.http.response import HttpResponse
from skyscanner.skyscanner import Flights
from django.template.defaultfilters import pprint

flights_service = Flights('sk183163813532396485407386558735')
result = flights_service.get_result(
    country='UK',
    currency='GBP',
    locale='en-GB',
    originplace='SIN-sky',
    destinationplace='KUL-sky',
    outbounddate='2017-05-28',
    inbounddate='2017-05-31',
    adults=1).parsed
pprint(result)
    
    