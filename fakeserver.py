#!/usr/bin/env python3

# Fake Server. Just says 'success'
import binascii
import socket
import struct
import time
import string
import logging
from crccheck.crc import Crc16Modbus

logging.basicConfig(format='%(asctime)s - %(levelname)s %(name)s %(message)s',level=logging.DEBUG)

socket.setdefaulttimeout(60)

def server_program():
    # get the hostname
    host = '10.1.1.35' # socket.gethostname()
    port = 7777 # initiate port no above 1024
    #host = '127.0.0.1' # socket.gethostname()
    #port = 7778 # initiate port no above 1024


    server_socket = socket.socket()  # get instance
    # look closely. The bind() function takes tuple as argument
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))  # bind host address and port together

    # configure how many client the server can listen simultaneously
    server_socket.listen(2)
    try:
        conn, address = server_socket.accept()  # accept new connection
    except socket.timeout:
        logging.error("Connection Timed out. Breaking", exc_info=True)
        return
    logging.info("Connection from: " + str(address))
    while True:
        # receive data stream. it won't accept data packet greater than 1024 bytes
        try:
            data = conn.recv(1024) #.decode('ascii','ignore')
        except ConnectionResetError:
            logging.error("ConnectionResetError: Connection lost. Breaking", exc_info=True)
            break
        except socket.timeout:
            logging.error("Connection Timed out. Breaking", exc_info=True)
            break

        if not data:
            # if data is not received break
            break

        # ! = network type - big endian
        # 3b = 3 x signed byes (commands)
        # i = 4 byte integer (length)
        header_format = "!3bi"
        header_size = struct.calcsize(header_format)

        if len(data) < header_size:
            # we don't seem to have a header, break out
            logging.error(f'Error in Header Size! Received Data Length: {len(data)}, Expected Minimum: {header_size} ', exc_info=True)
            logging.debug("RECEIVED: {}".format(data))
            break


        val1, val2, val3, length = struct.unpack_from(header_format, data, 0)

        checksumsize = 2

        #start reading actual data of format string length
        if length > 0:
            # check if length in headers is more than what we have
            # remove headers + checksum from size check
            while length > (len(data) - header_size - checksumsize):
                # read more data
                extradata = conn.recv(1024) #.decode('ascii','ignore')
                if not data:
                # if data is not received break
                    break
                data += extradata
            if length != len(data) - header_size - 2:
                logging.info(f'Error in received data! Length Expected: {length}, Actual Length of Data: {len(data) - header_size - 2}')
                logging.debug("RECEIVED: {}".format(data))
            format_string = f'!{length}sH'
            logging.debug(f'Format String: {format_string}')
            content, checksum = struct.unpack_from(format_string, data, header_size)
            crc = Crc16Modbus.calc(data[:-2])
            if crc != checksum:
                logging.error(f'Error in Checksum! Received: {checksum}, Expected: {crc}', exc_info=True)
                logging.debug("RECEIVED: {}".format(data))
                break
        else:
            logging.debug("RECEIVED: {}".format(data))
            logging.info(f'F1: {val1}, F2: {val2}, F3: {val3}, Length: {length}')
            continue



        # ! = network type - big endian
        # H = 2 byte unsigned short integer (checksum)
        #struct.unpack_from("!H", data, header_size + length) # at end of data

        logging.debug("RECEIVED: {}".format(data))
        logging.info(time.asctime(time.localtime(time.time())))
        logging.info(f'F1: {val1}, F2: {val2}, F3: {val3}, Length: {length}')
        logging.info(f'Content: {content}')

        # Response to auth
        if (val1 == 1, val2 == 1, val3 == 2):
            val2 = 2
            data = '{"Status":"Success"}'
        else:
            val2 = 2
            data = '{"Status":"Success"}'


        check = struct.pack('!3bi', val1, val2, val3, len(data)) + bytes(data, encoding='ascii')
        crc = Crc16Modbus.calc(check)
        check = check + struct.pack('!H',crc)

        # Now for the reply
        logging.debug("SENT: {}".format(check))
        # data = input(' -> ')
        conn.sendall(check)  # send data to the client


    conn.close()  # close the connection


if __name__ == '__main__':
    while True:
        server_program()
