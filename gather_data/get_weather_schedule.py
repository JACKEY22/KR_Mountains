#scheduler 1hour
import get_weather
import schedule, time

schedule.every(1).hours.do(get_weather.weather)
while 1:
    schedule.run_pending
    time.sleep(1)