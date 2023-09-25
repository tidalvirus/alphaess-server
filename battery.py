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
    received_command = []
    length = 0
    clock_drift = 0  # keep track of the time difference

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
        self.received_command = [val1, val2, val3]

    def reply(self) -> bytes:
        """_summary_

        Returns:
            str: _description_
        """

        # We should never hit this - we only expected commands with a '1' in this position
        if self.received_command[1] != 1:
            raise UserWarning

        data = (
            '{"Status":"Success"}'  # this is all we send to the battery at this stage
        )

        # Generate data for reply, and calculate checksum
        check = struct.pack(
            "!3bi",
            self.received_command[0],  # Always '1'
            2,  # All replies (from this server) are '2'
            self.received_command[2],
            len(data),
        ) + bytes(data, encoding="ascii")
        crc = Crc16Modbus.calc(check)
        return check + struct.pack("!H", crc)

    def checksum_is_valid(self, data) -> bool:
        """_summary_

        Args:
            data (_type_): _description_

        Returns:
            bool: _description_
        """
        format_string = f"!{self.length}sH"
        logging.debug("Format String: %s", format_string)

        received_checksum = struct.unpack_from(
            format_string, data, self.get_header_size()
        )[1]
        crc = Crc16Modbus.calc(data[:-2])
        if crc != received_checksum:
            logging.error(
                "Received Checksum: %d, Expected Checksum: %d",
                received_checksum,
                crc,
                exc_info=True,
            )
            logging.debug("RECEIVED: %s", format(data))
            return False
        else:
            logging.info("Checksum OK")
        return True
