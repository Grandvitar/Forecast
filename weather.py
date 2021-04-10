import requests
import datetime
import sys
import argparse
import json

APPID = 'cc2635d0b3d737c74a482d95669f0180'
CURRENT_WEATHER = 'http://api.openweathermap.org/data/2.5/weather'
WEEK_FORECAST = 'https://api.openweathermap.org/data/2.5/onecall?exclude=minutely,hourly'

def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('city')
    parser.add_argument('date', nargs='?')
    parser.add_argument('--file', nargs='?', type=argparse.FileType(mode='w'))
    return parser

parser = createParser()
namespace = parser.parse_args(sys.argv[1:])

def currentWeather():
    current = requests.get(CURRENT_WEATHER,
                           params={'q': namespace.city, 'units': 'metric', 'appid': APPID, 'lang': 'RU'}).json()
    return current

def showCurrentWeather(current):
    print(f'''Текущая температура в городе {current['name']},{current['sys']['country']} составляет {current['main']['temp']}, {current['weather'][0]['description']}
Ощущается как {current['main']['feels_like']}
Скоросто ветра: {current['wind']['speed']}
''')

def weekForecast(json):
    json_forecast = requests.get(WEEK_FORECAST, params={'lat': json['coord']['lat'], 'lon': json['coord']['lon'],
                                                        'appid': APPID,'units': 'metric', 'lang': 'RU'}).json()
    return json_forecast

def showWeather(json, json_forecast, date, i):
    print(f'''Прогноз на {date.strftime("%d.%m.%Y")} в {json['name']},{json['sys']['country']} следующий: 
    Дневная температура: {json_forecast['daily'][i]['temp']['day']}
    Ощущается: {json_forecast['daily'][i]['feels_like']['day']}
    Скорость ветра: {json_forecast['daily'][i]['wind_speed']}
    Осадки: {json_forecast['daily'][i]['weather'][0]['description']}
    УФ-индекс: {json_forecast['daily'][i]['uvi']}\n''')

def showWeekForecast(json, json_forecast):
    for _ in range(len(json_forecast['daily'])):
        timestamp = json_forecast['daily'][_]['dt']
        date = datetime.datetime.fromtimestamp(timestamp)
        showWeather(json, json_forecast, date, _)

def showDateForecast(json, json_forecast):
    input_date = datetime.datetime.strptime(namespace.date, '%d.%m.%Y')
    for i in range(len(json_forecast.get('daily'))):
        timestamp = json_forecast['daily'][i]['dt']
        date = datetime.datetime.fromtimestamp(timestamp)
        if input_date.day == date.day:
            showWeather(json, json_forecast, date, i)
            if namespace.file:
                importToFile(json_forecast, date, i)

def importToFile(json_forecast, date, i):
    info = {}
    info.update({'Прогноз на дату: ': date.strftime("%d.%m.%Y")})
    info.update({'Название города: ': namespace.city})
    info.update({'Дневная температура: ': json_forecast['daily'][i]['temp']['day']})
    info.update({'Ощущается: ': json_forecast['daily'][i]['feels_like']['day']})
    info.update({'Скоросто ветра: ': json_forecast['daily'][i]['wind_speed']})
    info.update({'Осадки: ': json_forecast['daily'][i]['weather'][0]['description']})
    info.update({'УФ-индекс: ': json_forecast['daily'][i]['uvi']})
    j = json.dumps(info, indent=4, ensure_ascii=False)
    with open('log.json', 'w', encoding='utf-8') as file:
        file.write(j)
