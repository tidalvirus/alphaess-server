#!/usr/bin/env python3

import socket
import struct
import time
import string

def server_program():
    # get the hostname
    host = '127.0.0.1' # socket.gethostname()
    port = 7779  # initiate port no above 1024

    server_socket = socket.socket()  # get instance
    # look closely. The bind() function takes tuple as argument
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))  # bind host address and port together

    # configure how many client the server can listen simultaneously
    server_socket.listen(1)
    conn, address = server_socket.accept()  # accept new connection
    print("Connection from: " + str(address))
    while True:
        # receive data stream. it won't accept data packet greater than 1024 bytes
        data = conn.recv(2048).decode('ascii','ignore')
        if not data:
            # if data is not received break
            break
        #filtered_string = filter(lambda x: x in string.printable, str(data))
        #print("RECEIVED: " + str(filtered_string))
        print("RECEIVED: " + data)
        data = '{"Status":"Success"}'
        print("SENT: ", data)
        # data = input(' -> ')
        conn.send(data.encode())  # send data to the client

        # if data has {, it must be the beginning. Check if } is included in this string,
        #   if so, parse and dump. If not, temporarily store.
        # if data has }, it must be the end, if we previously had a {, merge with previous contents and dump
        # if data does not have any braces, it might be a CSV table, or it might be the middle of a large packet (or an unknown)


    conn.close()  # close the connection


if __name__ == '__main__':
    server_program()