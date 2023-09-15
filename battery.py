"""Decoding battery output"""

import logging

import struct
from crccheck.crc import Crc16Modbus

logging.basicConfig(
    format="%(asctime)s - {%(pathname)s:%(lineno)d} - %(levelname)s %(name)s %(message)s",
    level=logging.DEBUG,
)


HEADER_FORMAT = "!3bi"
CHECKSUM_SIZE = 2


class Battery:
    """Methods to work with an Alpha ESS battery"""

    current_command = []

    def get_header_size(self) -> int:
        """Return length of battery comms header

        Returns:
            int: header length
        """ """"""

        header_size = struct.calcsize(HEADER_FORMAT)
        return header_size

    def commands(self, data):
        """_summary_

        Args:
            data (_type_): _description_
        """
        val1, val2, val3, length = struct.unpack_from(HEADER_FORMAT, data, 0)
        self.current_command = [val1, val2, val3]

        return length

    def reply(self) -> bytes:
        """_summary_

        Returns:
            str: _description_
        """

        self.current_command[1] = 2  # switch it to a reply
        data = (
            '{"Status":"Success"}'  # this is all we send to the battery at this stage
        )

        check = struct.pack(
            "!3bi",
            self.current_command[0],
            self.current_command[1],
            self.current_command[2],
            len(data),
        ) + bytes(data, encoding="ascii")
        crc = Crc16Modbus.calc(check)
        check = check + struct.pack("!H", crc)

        return check

    def checksum_is_valid(self, data) -> bool:
        """_summary_

        Args:
            data (_type_): _description_

        Returns:
            bool: _description_
        """
        format_string = f"!{self.commands(data)}sH"
        logging.debug("Format String: %s", format_string)
        content, checksum = struct.unpack_from(
            format_string, data, self.get_header_size()
        )
        crc = Crc16Modbus.calc(data[:-2])
        if crc != checksum:
            logging.error(
                "Error in Checksum! Received: %d, Expected: %d",
                checksum,
                crc,
                exc_info=True,
            )
            logging.debug("RECEIVED: %s", format(data))
            return False
        else:
            logging.info("Checksum fine")
        return True
