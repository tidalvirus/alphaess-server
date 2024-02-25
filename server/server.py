#!/usr/bin/env python3
""" Threaded server to fake www.alphaess.com port 7777 
that batteries sync data to"""

# import binascii
# import socket
import threading
import socketserver

# import struct
# import sys
# import re
# import time
import logging

from battery import Battery

# import json
# from datetime import datetime

# from crccheck.crc import Crc16Modbus


# from influxdb_client import InfluxDBClient, Point, WritePrecision
# from influxdb_client.client.write_api import SYNCHRONOUS

logging.basicConfig(
    format="%(asctime)s - {%(pathname)s:%(lineno)d} - %(levelname)s %(name)s %(message)s",
    level=logging.DEBUG,
)


HOST, PORT = "localhost", 7778


class BatteryTCPHandler(socketserver.BaseRequestHandler):
    """class to handle comms with the battery"""

    def handle(self):
        this_battery = Battery()
        self.request.settimeout(30)
        # print(f"This battery is battery: {this_battery}")

        logging.info("Active threads: %d", threading.active_count())
        while True:
            try:
                data = self.request.recv(1024)  # , "ascii")
            except ConnectionResetError:
                logging.error(
                    "ConnectionResetError: Connection lost. Breaking", exc_info=False
                )
                # self.server.close_request(self.request)
                break
            except TimeoutError:
                logging.error("Connection Timed out. Breaking", exc_info=True)
                break

            if not data:
                # if data is not received break
                break

            if len(data) < this_battery.get_header_size():
                logging.error(
                    "Error in Header Size. Received Data Length: %d, Expected Minimum: %d ",
                    len(data),
                    this_battery.get_header_size(),
                    exc_info=True,
                )
                break
            this_battery.get_command_and_length(data)
            length = this_battery.length  # need length of rest of data

            if length > 0:  # if the battery is sending data, not just a command
                data = self.get_extra_data(this_battery, data=data, length=length)
                if (
                    length
                    != len(data)
                    - this_battery.get_header_size()
                    - this_battery.CHECKSUM_SIZE
                ):
                    logging.error(
                        "Error in received data! Length Expected: %d, Actual Length of Data: %d",
                        length,
                        len(data)
                        - this_battery.get_header_size()
                        - this_battery.CHECKSUM_SIZE,
                    )
                    logging.debug("RECEIVED: %s", format(data))
                    break
                if this_battery.checksum_is_valid(data) is True:
                    logging.debug("RECEIVED valid checksum: %s", format(data))

            else:
                logging.debug("RECEIVED: %s", format(data))
                logging.info(
                    "F1: %d, F2: %d, F3: %d, Length: %d",
                    this_battery.command_field[0],
                    this_battery.command_field[1],
                    this_battery.command_field[2],
                    length,
                )

            this_battery.handle_command(data)
            response = this_battery.reply()
            self.request.sendall(response)
            # cur_thread = threading.current_thread()
            # response = bytes("{}: {}".format(cur_thread.name, data), "ascii")
            # print(f"{response}")
            # self.request.sendall(response)

    def get_extra_data(self, battery: Battery, data: bytes, length: int) -> bytes:
        """Get any extra data that was not received in the first request

        Args:
            battery (Battery): the Battery object
            data (bytes): the original data
            length (int): the total length of the data expected

        Returns:
            bytes: the extra data added onto the original data
        """
        while length > (len(data) - battery.get_header_size() - battery.CHECKSUM_SIZE):
            try:
                extradata = self.request.recv(1024)  # .decode('ascii','ignore')
            except ConnectionResetError:
                logging.error(
                    "ConnectionResetError: Connection lost. Breaking",
                    exc_info=True,
                )
                break
            except TimeoutError:
                logging.error("Connection Timed out. Breaking", exc_info=True)
                break
            if not data:
                # if data is not received break
                logging.error("No data received", exc_info=True)
                break
            data += extradata
        return data


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    """Threaded TCP Server to be used by the Battery TCP Handler"""

    allow_reuse_address = True

    def handle_error(self, request, client_address):
        """handle any exception that may occur"""
        logging.exception("Exception occurred", exc_info=True)
        #

        # print(f"An error occurred processing request from: {client_address}")

    # def handle_timeout(self):
    #     """Handle the case when no request is received within timeout"""

    #     print(f"No request received within {self.request.server.timeout} seconds")


if __name__ == "__main__":
    server = ThreadedTCPServer((HOST, PORT), BatteryTCPHandler)
    server.timeout = 10
    # with server:
    ip, port = server.server_address
    print(f"Server running on {ip}:{port}")
    # Start a thread with the server -- that thread will then start one
    # more thread for each request
    server_thread = threading.Thread(target=server.serve_forever)
    # Exit the server thread when the main thread terminates
    # server_thread.daemon = True
    server_thread.start()
    print("Server loop running in thread:", server_thread.name)
    # time.sleep(60)
    # server.shutdown()
