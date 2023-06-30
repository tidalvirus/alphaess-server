#!/usr/bin/env python3
""" Basic script to parse the 5 minute outputs from fakeserver.py
Just read the data from tailed log file
tail -F <logfile> | other-monitor.py"""

import sys, re, json, os

from datetime import datetime

from influxdb_client import InfluxDBClient  # , Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

# You can generate a Token from the "Tokens Tab" in the UI
from dotenv import load_dotenv

load_dotenv()


# You can generate a Token from the "Tokens Tab" in the UI
token = os.environ.get("INFLUXDB_OTHER_TOKEN")
org = os.environ.get("INFLUXDB_ORG")
bucket = os.environ.get("INFLUXDB_OTHER_BUCKET")
influx_host = os.environ.get("INFLUXDB_HOST")

client = InfluxDBClient(url=influx_host, token=token)  # type: ignore
write_api = client.write_api(write_options=SYNCHRONOUS)


# p = re.compile(r'(Content): \{(.*)\}')


for line in sys.stdin:
    line = line.strip()
    m = re.match(r".*F1: 1, F2: 1, F3: 5.*(Content).*(\{.*\})", line)
    if m:
        battery_info = json.loads(m.group(2))
        time_now = datetime.now()
        seconds, _ = str(time_now.timestamp()).split(".")

        data = ""
        for k, v in battery_info.items():
            if k == "Time":
                continue
            if k == "SN":
                continue
            if k == "CSQ":
                data += f'{k}="{v}",'
                continue
            if k == "EmsStatus":
                data += f'{k}="{v}",'
                continue
            data += f"{k}={v},"

        data = data[:-1]
        beginning = "battery "
        ending = f" {seconds}"
        write_api.write(bucket, org, beginning + data + ending, "s")  # type: ignore
        print(beginning + data + ending)


def live_info():
    pass
