import requests
from datetime import datetime

API_KEY = "dac73cd4aa6d251af51224cd3e8983c9"
CITY = "Istanbul"
url = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}"
print(url)
resp = requests.get(url)
resp = resp.json()
data = {}
data['date'] = datetime.utcfromtimestamp(resp['dt']).strftime('%m-%d-%Y %H:%M')
data['windspeed'] = resp['wind']['speed']
data['winddir'] = resp['wind']['deg']
data['temp'] = round(resp['main']['temp']-273.15,3)
data['mintemp'] = round(resp['main']['temp_min']-273.15,3)
data['maxtemp'] = round(resp['main']['temp_max']-273.15,3)

print(data)
