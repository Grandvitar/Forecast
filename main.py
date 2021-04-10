import weather
import datetime

current = weather.currentWeather()
json_forecast = weather.weekForecast(current)

date_now = datetime.datetime.today()

def main():
    if not weather.namespace.date:
        weather.showCurrentWeather(current)
        weather.showWeekForecast(current, json_forecast)
    elif (datetime.datetime.strptime(weather.namespace.date, '%d.%m.%Y') - date_now) > datetime.timedelta(7):
        print('***Прогноз можно запросить только на ближайшие 7 дней***')
    else:
        weather.showDateForecast(current, json_forecast)

main()
