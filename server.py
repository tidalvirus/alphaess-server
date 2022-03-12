#!/usr/bin/env python3

#Server to fake www.alphaess.com port 7777 that batteries sync data to

import binascii
import socket
import struct
import sys
import re
import json
from crccheck.crc import Crc16Modbus

from datetime import datetime

from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS


HOST, PORT = "localhost", 7778

def server_program():
    server_socket = socket.socket() # get instance
    # look closely. The bind() function takes tuple as argument
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))  # bind host address and port together

    # configure how many client the server can listen simultaneously
    server_socket.listen(1)
    conn, address = server_socket.accept()  # accept new connection
    print("Connection from: " + str(address))
    while True:


if __name__ == '__main__':
    server_program()