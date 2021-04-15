#!/usr/bin/env python3

#Fake Battery (client)

import binascii
import socket
import struct
import sys
import re
import time
from crccheck.crc import Crc16Modbus


# Server details
HOST, PORT = "localhost", 7778

#filename = "1-1-16.direct.json"

# Create a socket (SOCK_STREAM means a TCP socket)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    # Connect to server and send data
    sock.connect((HOST, PORT))

    files = ['1-1-2.direct.json', '1-1-9.direct.json', '1-1-16.direct.json', '1-2-3.direct.json', '1-1-4.direct.json']
    for filename in files:

        with open(filename, 'rb') as f:
            data = f.read()
        f.close()
        length = len(data)

        values = re.split(r'[.-]', filename)
        val1, val2, val3 = int(values[0]), int(values[1]), int(values[2])

        #count the length, and mimic the data the battery might actually send
        check = struct.pack("!3bi", val1, val2, val3, length) + bytes(data)
        crc = Crc16Modbus.calc(check)
        check = check + struct.pack('!H',crc)

        sock.sendall(check)
        print("Sent:     {}".format(check))
        print("Sleeping...")
        time.sleep(1)


    # Receive data from the server and shut down
    #received = str(sock.recv(1024), "utf-8")

#print("Sent:     {}".format(check))
#print("Received: {}".format(received))