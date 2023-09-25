#!/usr/bin/env python3
""" Basic script to parse the 10 second outputs from fakeserver.py
Just read the data from tailed log file
tail -F <logfile> | battery-monitor.py"""
# pylint: disable=invalid-name

import sys, re, json, time, os

from datetime import datetime

from influxdb_client import InfluxDBClient  # , Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

from dotenv import load_dotenv

load_dotenv()


# You can generate a Token from the "Tokens Tab" in the UI
token = os.environ.get("INFLUXDB_TOKEN")
org = os.environ.get("INFLUXDB_ORG")
bucket = os.environ.get("INFLUXDB_BUCKET")
influx_host = os.environ.get("INFLUXDB_HOST")

client = InfluxDBClient(url=influx_host, token=token)  # type: ignore
mywrite_api = client.write_api(write_options=SYNCHRONOUS)


FILENAME = sys.argv[1]

# p = re.compile(r'(Content): \{(.*)\}')

HTMLHEAD = "<html><head><title>Battery Info</title></head><body>"
HTMLFOOT = "</body></html>"
clock_drift = 0
for line in sys.stdin:
    line = line.strip()
    m = re.match(r'.*(Content).*(\{.*"SOC":"\d+\.\d"\})', line)
    if m:
        battery_info = json.loads(m.group(2))

        if clock_drift == 0:
            # Let's calculate clock drift
            time_now = datetime.now()
            clock_drift = (
                datetime.strptime(battery_info["Time"], "%Y/%m/%d %H:%M:%S") - time_now
            )

        # print(f'Group 2 {m.group(2)}')
        # for key, value in battery_info.items():
        #    print(f'Key: {key}, Value: {value}')
        battery_time = datetime.strptime(battery_info["Time"], "%Y/%m/%d %H:%M:%S")
        calculated_drift = battery_time - clock_drift
        f = open(FILENAME, "w", encoding="utf-8")
        f.write(HTMLHEAD)
        f.write(f'<p>Battery: {battery_info["SOC"]}%</p>')
        f.write(f'<p>Current Usage?: {battery_info["Sva"]}</p>')
        f.write(f'<p>Grid Usage?: {battery_info["PmeterL1"]}</p>')
        f.write(f'<p>Panels 1: {battery_info["Ppv1"]}</p>')
        f.write(f'<p>Panels 2: {battery_info["Ppv2"]}</p>')
        f.write(f'<p>PrealL1?: {battery_info["PrealL1"]}</p>')
        f.write(f'<p>Battery Usage: {battery_info["Pbat"]}</p>')
        f.write(f'<p>Battery Time: {battery_info["Time"]}</p>')
        f.write(f"<p>Calculated Drift: {calculated_drift}</p>")
        f.write(f"<p>Last Update: {time.asctime(time.localtime(time.time()))}")
        f.write("<pre>")
        for k, v in battery_info.items():
            if k == "SN":
                continue
            f.write(f"{k}: {v}\n")
        f.write("</pre>")
        f.write(HTMLFOOT)
        f.close()

        seconds, _ = str(calculated_drift.timestamp()).split(".")

        data = ""
        for k, v in battery_info.items():
            if k == "Time":
                continue
            if k == "SN":
                continue
            data += f"{k}={v},"

        data = data[:-1]
        beginning = "battery "
        ending = f" {seconds}"
        mywrite_api.write(bucket, org, beginning + data + ending, "s")  # type: ignore
        print(beginning + data + ending)
