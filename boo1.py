from tkinter import *
import datetime
from weather import Weather, Unit

prev_date = datetime.datetime.today() - datetime.timedelta(days=1)
prev_date_format = prev_date.strftime ('%Y-%m-%d') 
print ('Previous Date: ' + str(prev_date_format))

print("/nMichal to rowny gosc")

"""
weather = Weather(unit=Unit.CELSIUS)

location = weather.lookup_by_location('dublin')
forecasts = location.forecast
for forecast in forecasts:
    print(forecast.text)
    print(forecast.date)
    print(forecast.high)
    print(forecast.low)
    
"""

"""
root = Tk()
theLabel = Label(root, text="Michal is the best")
theLabel.pack()
second = Label(root, text="Kolejny text comes here")
second.pack()
root.mainloop()
"""
