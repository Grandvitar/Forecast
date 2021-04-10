import weather
import datetime

json = weather.currentWeather()
json_forecast = weather.weekForecast(json)

date_now = datetime.datetime.today()

def main():
    if not weather.namespace.date:
        weather.showCurrentWeather(json)
        weather.showWeekForecast(json, json_forecast)
    elif (datetime.datetime.strptime(weather.namespace.date, '%d.%m.%Y') - date_now) > datetime.timedelta(7):
        print('***Прогноз можно запросить только на ближайшие 7 дней***')
    else:
        weather.showDateForecast(json, json_forecast)

main()
