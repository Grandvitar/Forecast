import requests
import datetime
import sys
import argparse
import json

appid = 'cc2635d0b3d737c74a482d95669f0180'

def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('city')
    parser.add_argument('date', nargs='?')
    parser.add_argument('--file', nargs='?', type=argparse.FileType(mode='w'))
    return parser

parser = createParser()
namespace = parser.parse_args(sys.argv[1:])

date_now = datetime.datetime.today()
limit = datetime.timedelta(7)
max_forecast = date_now + limit

def currentWeather():
    try:
        json = requests.get('http://api.openweathermap.org/data/2.5/weather',
                        params={'q': namespace.city, 'units':'metric', 'appid':appid, 'lang':'RU'}).json()
        global lon
        lon = json['coord']['lon']
        global lat
        lat = json['coord']['lat']
        global country
        country = json['sys']['country']
        print(f'''Текущая температура в городе {namespace.city},{country} составляет {json['main']['temp']}, {json['weather'][0]['description']}
        Ощущается как {json['main']['feels_like']}
        Скоросто ветра: {json['wind']['speed']}
        ''')
    except Exception as e:
        print ('Найдена ошибка: ', e)

def fixDateForecast():
    global date, temp_day, temp_feelslike, wind_speed, weather, uv
    input_date = datetime.datetime.strptime(namespace.date, '%d.%m.%Y')
    json_forecast = requests.get('https://api.openweathermap.org/data/2.5/onecall?exclude=minutely,hourly',
    params={'lat': lat, 'lon': lon, 'appid': appid, 'units': 'metric', 'lang': 'RU'}).json()
    if (input_date - date_now) > limit:
        print('***Прогноз можно запросить только на ближайшие 7 дней***')
    for i in range(len(json_forecast.get('daily'))):
        timestamp = json_forecast['daily'][i]['dt']
        date = datetime.datetime.fromtimestamp(timestamp)
        if input_date.day == date.day:
            temp_day = json_forecast['daily'][i]['temp']['day']
            temp_feelslike = json_forecast['daily'][i]['feels_like']['day']
            wind_speed = json_forecast['daily'][i]['wind_speed']
            weather = json_forecast['daily'][i]['weather'][0]['description']
            uv = json_forecast['daily'][i]['uvi']
            print(f'''Прогноз на {date.strftime("%d.%m.%Y")} в {namespace.city},{country} следующий: 
    Дневная температура: {temp_day}
    Ощущается: {temp_feelslike}
    Скорость ветра: {wind_speed}
    Осадки: {weather}
    УФ-индекс: {uv}\n''')

def weekForecast():
    global date, temp_day, temp_feelslike, wind_speed, weather, uv
    json_forecast = requests.get('https://api.openweathermap.org/data/2.5/onecall?exclude=minutely,hourly',
    params={'lat': lat, 'lon': lon, 'appid': appid, 'units': 'metric', 'lang': 'RU'}).json()
    for i in range(len(json_forecast.get('daily'))):
        timestamp = json_forecast['daily'][i]['dt']
        date = datetime.datetime.fromtimestamp(timestamp)
        temp_day = json_forecast['daily'][i]['temp']['day']
        temp_feelslike = json_forecast['daily'][i]['feels_like']['day']
        wind_speed = json_forecast['daily'][i]['wind_speed']
        weather = json_forecast['daily'][i]['weather'][0]['description']
        uv = json_forecast['daily'][i]['uvi']
        print(f'''Прогноз на {date.strftime("%d.%m.%Y")} в {namespace.city},{country} следующий: 
    Дневная температура: {temp_day}
    Ощущается: {temp_feelslike}
    Скорость ветра: {wind_speed}
    Осадки: {weather}
    УФ-индекс: {uv}\n''')

def saveToFile():
    info = {}
    info.update({'Прогноз на дату: ': str(date)})
    info.update({'Название города: ': namespace.city})
    info.update({'Дневная температура: ': temp_day})
    info.update({'Ощущается: ': temp_feelslike})
    info.update({'Скоросто ветра: ': wind_speed})
    info.update({'Осадки: ': weather})
    info.update({'УФ-индекс: ': uv})
    j = json.dumps(info, indent=4, ensure_ascii=False)
    with open ('log.json', 'w', encoding='utf-8') as file:
        file.write(j)






