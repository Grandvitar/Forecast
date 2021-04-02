import requests
import datetime
import sys
import argparse

def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('city')
    return parser

if __name__ == '__main__':
    parser = createParser()
    namespace = parser.parse_args(sys.argv[1:])

print(namespace.city)

appid = 'cc2635d0b3d737c74a482d95669f0180'
json = requests.get('http://api.openweathermap.org/data/2.5/weather',
                    params={'q': namespace.city, 'units':'metric', 'appid':appid, 'lang':'RU'}).json()
lon = json['coord']['lon']
lat = json['coord']['lat']
print(f'''Текущая температура в городе {namespace.city} составляет {json['main']['temp']}, {json['weather'][0]['description']}
Ощущается как {json['main']['feels_like']}
Скоросто ветра: {json['wind']['speed']}
''')
json_forecast = requests.get('https://api.openweathermap.org/data/2.5/onecall?exclude=minutely,hourly',
                    params={'lat': lat, 'lon': lon, 'appid': appid, 'units': 'metric',
                            'lang': 'RU'}).json()
for i in range(len(json_forecast.get('daily'))):
    timestamp = json_forecast['daily'][i]['dt']
    date = datetime.datetime.fromtimestamp(timestamp)
    temp_day = json_forecast['daily'][i]['temp']['day']
    temp_feelslike = json_forecast['daily'][i]['feels_like']['day']
    wind_speed = json_forecast['daily'][i]['wind_speed']
    weather = json_forecast['daily'][i]['weather'][0]['description']
    uv = json_forecast['daily'][i]['uvi']
    print(date.strftime('%Y-%m-%d %H:%M:%S'))
    print(f'''Дневная температура: {temp_day}
Ощущается: {temp_feelslike}
Скорость ветра: {wind_speed}
Осадки: {weather}
УФ-индекс: {uv}\n''')



# if __name__ == "__main__":
#     for param in sys.argv:
#         print (param)