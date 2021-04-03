#!/usr/bin/env python3

# Read a raw dumped file from an alphaess battery and server communication pcap
from struct import *
#from struct import unpack, pack
import sys
import os
from crccheck.crc import Crc16Modbus

# Read a fixed number of bytes, dictated by "l"
def read_bytes(f, l):
    bytes = f.read(l)
    if len(bytes) != l:
        print("Expected: %d, Only received: %d" % (l, len(bytes)))
        raise Exception("Not enough bytes in stream")
    return bytes

# Unpack a 4 byte integer in network byte order
def read_int(f):
    return unpack("!i", read_bytes(f, 4))[0]

# Read a single byte
def read_byte(f):
    return ord(read_bytes(f, 1))

# Read checksum (2 bytes)
def read_checksum(f):
    return int.from_bytes(read_bytes(f, 2), "big")

filename = sys.argv[1]
file_size = os.path.getsize(filename)

f = open(filename, "rb")
#print ("Connection: %s" % read_bytes(f, 4))

# Keep reading until file is empty.
while f.tell() < file_size:
    val1 = read_byte(f)
    val2 = read_byte(f)
    val3 = read_byte(f)
    length = read_int(f)
    if length > 0:
        data = read_bytes(f, length)
    else:
        data = b''
    checksum = read_checksum(f)
 

    check = pack('>bbbi', val1, val2, val3, length)
    check = check + data
    #print("Size: %s, contents: %s" % (calcsize('>bbbi'), check))
    crc = Crc16Modbus.calc(check)

    #print("calculated CRC: %d" % (crc))
    if crc == checksum:
        match = "Y"
    else:
        match = "N"
    #print("Val1: %d, Val2: %d, Val3: %d, Len: %d, Data: %20s, CRC: %d, CRC: %s" % (val1, val2, val3, length, data, checksum, match))
    print(f'Val1: {val1}, Val2: {val2}, Val3: {val3}, Len: {length}, Data: {data}, CRC: {checksum}, Match: {match}')


# lets just test we've got the right crc check
# double checking against the website results in https://www.scadacore.com/tools/programming-calculators/online-checksum-calculator/
# should be 11 0A - website says little endian, but is actually big endian.
#print("Test CRC: %d" % (Crc16Modbus.calc(b'\x01\x01\x00\x00\x00\x00\x00')))