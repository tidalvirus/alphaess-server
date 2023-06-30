import time
from datetime import datetime

battery_time = "2021/04/29 21:57:57"
time_now = datetime.today()

print(f'Now: {time_now} / {time_now.timestamp()}')

battery_time = datetime.strptime(battery_time, "%Y/%m/%d %H:%M:%S")

print(f'Battery: {battery_time} / {battery_time.timestamp()}')
adjusted_time = battery_time - time_now

print(f'Difference: {adjusted_time}')

# for future reads, now just use the adjusted time to calculate current time.
times = "2021/04/29 21:57:17", "2021/04/29 21:57:27", "2021/04/29 21:57:37", "2021/04/29 21:57:47", "2021/04/29 21:57:57"
for i in times:
    battery = datetime.strptime(i, "%Y/%m/%d %H:%M:%S")
    adjusted = battery - adjusted_time
    string1 = f'Adjusted time: {adjusted.timestamp()}'
    seconds, _ = str(adjusted.timestamp()).split('.')
    string2 = f'Just seconds: {seconds}'
    print(string1, string2)



""" from rickspencer:

def send_line(line):
    url = "{}api/v2/write?org={}&bucket={}&precision={}".format(influx_url, organization, bucket, precision)
    headers = {"Authorization": "Token {}".format(influx_token)}
    r = requests.post(url, data=line, headers=headers) """