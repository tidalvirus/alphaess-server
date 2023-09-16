"""Decoding battery output"""

import logging

import struct
from crccheck.crc import Crc16Modbus

logging.basicConfig(
    format="%(asctime)s - {%(pathname)s:%(lineno)d} - %(levelname)s %(name)s %(message)s",
    level=logging.DEBUG,
)


class Battery:
    """Methods to work with an Alpha ESS battery"""

    HEADER_FORMAT = "!3bi"
    CHECKSUM_SIZE = 2
    current_command = []
    length = 0

    def get_header_size(self) -> int:
        """Return length of battery comms header

        Returns:
            int: header length
        """ """"""

        header_size = struct.calcsize(self.HEADER_FORMAT)
        return header_size

    def get_command(self, data):
        """_summary_

        Args:
            data (_type_): _description_
        """
        val1, val2, val3, self.length = struct.unpack_from(self.HEADER_FORMAT, data, 0)
        self.current_command = [val1, val2, val3]

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
        format_string = f"!{self.length}sH"
        logging.debug("Format String: %s", format_string)
        checksum = struct.unpack_from(format_string, data, self.get_header_size())[1]
        crc = Crc16Modbus.calc(data[:-2])
        if crc != checksum:
            logging.error(
                "Received Checksum: %d, Expected Checksum: %d",
                checksum,
                crc,
                exc_info=True,
            )
            logging.debug("RECEIVED: %s", format(data))
            return False
        else:
            logging.info("Checksum OK")
        return True
