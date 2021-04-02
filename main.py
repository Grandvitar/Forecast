import first

def main():
    first.createParser()
    if not first.namespace.date:
        first.currentWeather()
        first.weekForecast()
    else:
        first.currentWeather()
        first.fixDateForecast()
    if first.namespace.file:
        first.saveToFile()

main()
