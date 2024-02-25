"""Decoding battery output"""

import dataclasses
import logging
import struct
import json
from dataclasses import dataclass
from enum import Enum

from crccheck.crc import Crc16Modbus

logging.basicConfig(
    format="%(asctime)s - {%(pathname)s:%(lineno)d} - %(levelname)s %(name)s %(message)s",
    level=logging.DEBUG,
)


class BatteryCommandType(Enum):
    """Enum for battery commands"""

    BATTERYDUMP = 5
    BATTERYDATA = 16


class Battery:
    """Methods to work with an Alpha ESS battery"""

    HEADER_FORMAT = "!3bi"
    CHECKSUM_SIZE = 2
    command_field = []
    length = 0
    clock_drift = 0  # keep track of the time difference

    def get_header_size(self) -> int:
        """Return length of battery comms header

        Returns:
            int: header length
        """

        header_size = struct.calcsize(self.HEADER_FORMAT)
        return header_size

    def get_command_and_length(self, data):
        """Extract command and length of data from received data

        Args:
            data (_type_): packed binary data containing command
        """
        val1, val2, val3, self.length = struct.unpack_from(self.HEADER_FORMAT, data, 0)
        self.command_field = [val1, val2, val3]

    def get_data(self, data: bytes) -> str:
        """Extract data from received data. This should only be called after a checksum
        has been validated with checksum_is_valid()

        Args:
            data (bytes): packed binary data containing data
        """
        format_string = f"!{self.length}sH"
        logging.debug("Format String: %s", format_string)

        content = struct.unpack_from(format_string, data, self.get_header_size())[0]

        return content

    def get_attribute_name(self, key):
        """Convert two letter keys from the battery to longer names"""
        if key == "SN":
            return "serial"
        elif key == "Ua":
            return "battery_ua"
        elif key == "Ub":
            return "battery_ub"
        elif key == "Uc":
            return "battery_uc"
        # Otherwise, return the key as it is
        else:  # return a lowercased key
            return key.lower()

    def reply(self) -> bytes:
        """Handles replies from the battery

        Returns:
            bytes: reply to send to battery
        """

        # We should never hit this - we only expected commands with a '1' in this position
        if self.command_field[1] != 1:
            raise UserWarning

        data = (
            '{"Status":"Success"}'  # this is all we send to the battery at this stage
        )

        # Generate data for reply, and calculate checksum
        check = struct.pack(
            "!3bi",
            self.command_field[0],  # Always '1'
            2,  # All replies (from this server) are '2'
            self.command_field[2],
            len(data),
        ) + bytes(data, encoding="ascii")
        crc = Crc16Modbus.calc(check)
        return check + struct.pack("!H", crc)

    def checksum_is_valid(self, data: bytes) -> bool:
        """Check if the checksum is valid

        Args:
            data (bytes): binary data to check

        Returns:
            bool: True if checksum is valid, False otherwise
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

    def handle_command(self, data: bytes) -> bool:
        """Handle the command received from the battery

        Returns:
            bool: True if successful, False otherwise
        """
        if self.command_field[0] == 1 and self.command_field[1] == 1:
            if self.command_field[2] == BatteryCommandType.BATTERYDUMP.value:
                logging.info("Data Dump received")
                self.get_battery_dump(self.get_data(data))
                return True
            elif self.command_field[2] == BatteryCommandType.BATTERYDATA.value:
                logging.info("Regular Data received")
                self.get_battery_data(self.get_data(data))
                return True
            else:
                logging.error("Unhandled command received")
                return False
        else:
            logging.error("Unhandled command received")
            return False

    def get_battery_data(self, data: str) -> bool:
        """Store the most recent 10 second dump from the battery in the dataclass

        Args:
            data: Bytes from the battery, minus the checksum and commands.

        Returns:
            bool: True if successful read, False otherwise
        """
        hashed = json.loads(data)
        latest_battery_data = BatteryData("", "", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
        for key, value in hashed.items():
            setattr(latest_battery_data, self.get_attribute_name(key), value)
            logging.debug("Key: %s, Value: %s", key, value)
        logging.debug("Latest Battery Data: %s", latest_battery_data)
        latest_battery_data = dataclasses.make_dataclass("BatteryData", hashed.keys())
        logging.debug("Latest Battery Data - hashed.keys: %s", latest_battery_data)
        return False

    def get_battery_dump(self, data: str) -> bool:
        """Store the larger 5 minute data dump from the battery in the dataclass

        Args:
            data: Bytes from the battery, minus the checksum and commands.

        Returns:
            bool: True if successful read, False otherwise
        """
        loaded_json = json.loads(data)
        latest_battery_dump = BatteryDump(
            "",
            "",
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            "",
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            "",
        )
        for key, value in loaded_json.items():
            setattr(latest_battery_dump, self.get_attribute_name(key), value)
            logging.debug("Key: %s, Value: %s", key, value)
        latest_battery_dump = dataclasses.make_dataclass(
            "BatteryDump", ((k, type(v)) for k, v in loaded_json.items())
        )
        return False


## Creating the below may have been a design error.
# Likely to be removed in favour of dataclasses directly from battery data
@dataclass
class BatteryData:
    """Store the most recent 10 second dump from the battery"""

    time: str
    serial: str  # field 'SN'
    ppv1: int
    ppv2: int
    preall1: float
    preall2: float
    preall3: float
    pmeterl1: int
    pmeterl2: int
    pmeterl3: int
    pbat: float
    sva: int
    varac: int
    vardc: int
    soc: float


@dataclass
class BatteryDump:
    """The larger 5 minute data dump from the battery"""

    time: str
    battery_sn: str  # field 'SN'
    ppv1: int
    ppv2: int
    upv1: float
    upv2: float
    battery_ua: float  # field 'Ua'
    battery_ub: float  # field 'Ub'
    battery_uc: float  # field 'Uc'
    fac: float
    ubus: int
    preall1: float
    preall2: float
    preall3: float
    tinv: int
    pacl1: float
    pacl2: float
    pacl3: float
    invworkmode: int
    epvtotal: float
    einput: float
    eoutput: float
    echarge: float
    pmeterl1: int
    pmeterl2: int
    pmeterl3: int
    pmeterdc: int
    pbat: float
    soc: float
    batv: float
    batc: float
    flagbms: int
    bmswork: int
    pcharge: int
    pdischarge: int
    bmsrelay: int
    bmsnum: int
    vcelllow: int
    vcellhigh: int
    tcelllow: int
    tcellhigh: int
    idtempelover: int
    idtempeover: int
    idtempediffe: int
    idchargecurre: int
    iddischcurre: int
    idcellvolover: int
    idcellvollower: int
    idsoclower: int
    idcellvoldiffe: int
    batc1: float
    batc2: float
    batc3: float
    batc4: float
    batc5: float
    batc6: float
    soc1: float
    soc2: float
    soc3: float
    soc4: float
    soc5: float
    soc6: float
    errinv: int
    warinv: int
    errems: int
    errbms: int
    errmeter: int
    errbackupbox: int
    egridcharge: float
    edischarge: float
    emsstatus: str
    invbatv: float
    bmsshutdown: int
    bmurelay: int
    bmshardver1: int
    bmshardver2: int
    bmshardver3: int
    dispatchswitch: int
    pdispatch: int
    dispatchsoc: int
    dispatchmode: int
    pmeterdcl1: int
    pmeterdcl2: int
    pmeterdcl3: int
    meterdcua: float
    meterdcub: float
    meterdcuc: float
    eirp: int
    csq: str
