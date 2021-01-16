
import json
import requests
import sys
import pprint
#studying from here: https://automatetheboringstuff.com/2e/chapter16/


APPID = 'e4d0a3086160156af9fa5bec75573b7a'

#Compute location from command line arguments
if len(sys.argv) < 2:
    print('Usage: getOpenWaether.py city name, 2-letter_country_code')
    sys.exit()
location = str(''.join(sys.argv[1:]))

print('Downloading weather data from {}...\n'.format(location))



#TODO use geopy module to obtain latitude and longitude. Download from pip install geopy (2.1.0)
from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent='my_app')
coordinates = geolocator.geocode(location)
lat, lon = coordinates.latitude, coordinates.longitude

#Test case: Monterrey coordinates lat: 25.6667, lon: -100.3167

#TODO use openweather API to get city's weather data.
url = 'https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&appid={}&units=metric'.format(lat,lon,APPID)
response = requests.get(url)
response.raise_for_status()
weatherData = json.loads(response.text)

#TODO write a text file with JSON data
result_file = open('weatherData.py','w')
result_file.write('allData = ' + pprint.pformat(weatherData))
result_file.close()

#read JSON file contents
#import weatherData
#data = weatherData.allData


#TODO display today's and 5 days in advance weather information: "todays weather in [city] is: "
from datetime import datetime
for i in range(0,6):
    day_utc = weatherData['daily'][i]['dt'] #returns Time of the forecasted data, Unix, UTC
    day = datetime.fromtimestamp(day_utc)
    if i == 0:
        print('Today\'s weather in {} is: '.format(location))
        print('{:.0f}°C but it feels like {:.0f}°C'.format(weatherData['current']['temp'],weatherData['current']['feels_like']))
        print('And we also have a {}'.format(weatherData['current']['weather'][0]['description'])+ '\n')
    else:
        print('The weather in {} on {} is: '.format(location,day))
        print('Minimum of {:.0f}°C and maximum of {:.0f}°C'.format(weatherData['daily'][i]['temp']['min'],weatherData['daily'][i]['temp']['max']))
        print('With a chance of {}'.format(weatherData['daily'][i]['weather'][0]['description'])+ '\n')
