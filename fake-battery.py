#!/usr/bin/env python3

#Fake Battery (client)

import binascii
import socket
import struct
import sys
from crccheck.crc import Crc16Modbus


HOST, PORT = "localhost", 7778
filename = "1-1-16.direct.json"

with open(filename, 'rb') as f:
    data = f.read()
f.close()
length = len(data)
#print(f"Length: {length}.")

#print(f"Data: {data}")

val1, val2, val3 = 1, 1, 16

#count the length, and mimic the data the battery might actually send
check = struct.pack("!3bi", val1, val2, val3, length) + bytes(data)
#print("Pre Checksum Size: %s, contents: %s" % (struct.calcsize('>bbbis'), check))
crc = Crc16Modbus.calc(check)
check = check + struct.pack('!H',crc)
#check = struct.pack('>bbbisH', val1, val2, val3, length, data, crc)
#print("Post Checksum Size: %s, contents: %s" % (struct.calcsize('>bbbisH'), check))


#data = (val1, val2, val3, data, crc)

# Create a socket (SOCK_STREAM means a TCP socket)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    # Connect to server and send data
    sock.connect((HOST, PORT))
    sock.sendall(check)

    # Receive data from the server and shut down
    #received = str(sock.recv(1024), "utf-8")

print("Sent:     {}".format(check))
#print("Received: {}".format(received))