# from time import strptime
# from time import strftime
import datetime

date = "Tue Jun 05 2020 06:29:54 GMT-0400 (Eastern Daylight Time)"

day = datetime.datetime.strptime(date[0:33], '%a %b %d %Y %H:%M:%S %Z%z')
day3 = day.strftime("%d/%m/%Y")
day2 = day.strftime("%H:%M:%S")
print(day2)