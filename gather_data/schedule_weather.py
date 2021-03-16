#scheduler 1hour
import get_weather_data
import schedule, time

schedule.every(1).hours.do(get_weather_data.weather)
while 1:
    schedule.run_pending
    time.sleep(1)