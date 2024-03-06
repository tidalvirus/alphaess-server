import struct
from server.battery import Battery
import pytest


def test_get_header_size():
    battery = Battery()
    expected_header_size = struct.calcsize(battery.HEADER_FORMAT)
    assert battery.get_header_size() == expected_header_size


def test_get_command_and_length():
    battery = Battery()
    data = struct.pack(battery.HEADER_FORMAT, 1, 2, 3, 4) + bytes(
        "{'SN': '12345', 'Ua': 1, 'Ub': 2, 'Uc': 3}", encoding="ascii"
    )
    battery.get_command_and_length(data)
    assert battery.command_field == [1, 2, 3]
    assert battery.length == 4


def test_get_data():
    battery = Battery()
    data = "{'SN': '12345', 'Ua': 1, 'Ub': 2, 'Uc': 3}"
    header_and_data = struct.pack(battery.HEADER_FORMAT, 1, 2, 3, 4) + bytes(
        data, encoding="ascii"
    )
    battery.get_command_and_length(header_and_data)
    content = battery.get_data(header_and_data)
    assert isinstance(content, bytes)
    # Add additional assertions for the expected content of the extracted data


def test_get_attribute_name():
    battery = Battery()
    assert battery.get_attribute_name("SN") == "serial"
    assert battery.get_attribute_name("Ua") == "battery_ua"
    assert battery.get_attribute_name("Ub") == "battery_ub"
    assert battery.get_attribute_name("Uc") == "battery_uc"
    assert battery.get_attribute_name("Unknown") == "unknown"
    with pytest.raises(ValueError):
        battery.get_attribute_name("a")
    with pytest.raises(ValueError):
        battery.get_attribute_name("bb")


def test_reply():
    battery = Battery()
    data = "{'SN': '12345', 'Ua': 1, 'Ub': 2, 'Uc': 3}"
    header_and_data = struct.pack(battery.HEADER_FORMAT, 1, 1, 3, 4) + bytes(
        data, encoding="ascii"
    )
    battery.get_command_and_length(header_and_data)
    reply = battery.reply()
    assert isinstance(reply, bytes)
    # Add additional assertions for the expected reply content


def test_checksum_is_valid():
    battery = Battery()
    data = '{"Status":"Success"}'  # this is all we send to the battery at this stage
    header_and_data = (
        struct.pack(battery.HEADER_FORMAT, 1, 2, 16, 20)
        + bytes(data, encoding="ascii")
        + bytes((0x57, 0xAC))
    )
    battery.get_command_and_length(header_and_data)

    valid_checksum = battery.checksum_is_valid(header_and_data)
    assert valid_checksum is True


# def test_handle_command():
#     battery = Battery()
#     data = "{'SN': '12345', 'Ua': 1, 'Ub': 2, 'Uc': 3}"
#     header_and_data = struct.pack(battery.HEADER_FORMAT, 1, 1, 16, 4) + bytes(
#         data, encoding="ascii"
#     )
#     battery.get_command_and_length(header_and_data)
#     success = battery.handle_command(header_and_data)
#     assert success
#     # Add additional assertions for the expected behavior of handle_command


def test_set_battery_data():
    battery = Battery()
    data = '{"Time":"2024/03/03 22:05:21","SN":"AL0123456789012","Ppv1":"0","Ppv2":"0","PrealL1":"420","PrealL2":"0.0","PrealL3":"0.0","PmeterL1":"-4","PmeterL2":"0","PmeterL3":"0","PmeterDC":"0","Pbat":"539.4400","Sva":"405","VarAC":"-669","VarDC":"96","SOC":"38.0"}'
    header_and_data = (
        struct.pack(battery.HEADER_FORMAT, 1, 1, 16, 255)
        + bytes(data, encoding="ascii")
        + bytes((0x57, 0xAC))
    )
    battery.get_command_and_length(header_and_data)
    success = battery.handle_command(header_and_data)
    # success = battery.set_battery_data(data)
    assert success
    # Add additional assertions for the expected behavior of set_battery_data


# 2024-03-03 22:49:15,878 - INFO root F1: 1, F2: 1, F3: 5, Length: 1485, Content: b'{"Time":"2024/03/03 22:10:04","SN":"AL0123456789012","Ppv1":"0","Ppv2":"0","Upv1":"7.3","Upv2":"8.3","Ua":"238.8","Ub":"0.0","Uc":"0.0","Fac":"50.02","Ubus":"370","PrealL1":"380","PrealL2":"0.0","PrealL3":"0.0","Tinv":"34","PacL1":"5000","PacL2":"-483","PacL3":"0.0","InvWorkMode":"3","EpvTotal":"35348.5","Einput":"5221.20","Eoutput":"11371.20","Echarge":"9428.4","PmeterL1":"-7","PmeterL2":"0","PmeterL3":"0","PmeterDC":"0","Pbat":"495.5060","SOC":"37.6","BatV":"49.06","BatC":"10.10","FlagBms":"257","BmsWork":"1","Pcharge":"4949","Pdischarge":"4949","BmsRelay":"3","BmsNum":"1","VcellLow":"16911559","VcellHigh":"17108169","TcellLow":"17170460","TcellHigh":"16908317","IdTempelover":"0","IdTempEover":"0","IdTempediffe":"0","IdChargcurre":"0","IdDischcurre":"0","IdCellvolover":"0","IdCellvollower":"0","IdSoclower":"0","IdCellvoldiffe":"0","BatC1":"10.00","BatC2":"0.00","BatC3":"0.00","BatC4":"0.00","BatC5":"0.00","BatC6":"0.00","SOC1":"37.6","SOC2":"0.0","SOC3":"0.0","SOC4":"0.0","SOC5":"0.0","SOC6":"0.0","ErrInv":"0","WarInv":"0","ErrEms":"0","ErrBms":"0","ErrMeter":"0","ErrBackupBox":"0","EGridCharge":"169.5","EDischarge":"9081.1","EmsStatus":"Normal","InvBatV":"49.40","BmsShutdown":"0","BmuRelay":"0","BmsHardVer1":"0", "BmsHardVer2":"0", "BmsHardVer3":"0","DispatchSwitch":"0","Pdispatch":"0", "DispatchSoc":"0", "DispatchMode":"0","PMeterDCL1":"0","PMeterDCL2":"0", "PMeterDCL3":"0","MeterDCUa":"239.2","MeterDCUb":"0.0", "MeterDCUc":"0.0","Eirp":"-36","CSQ":"99,99"}'
def test_set_battery_dump():
    battery = Battery()
    data = '{"TTTTTTTime":"2024/03/03 22:10:04","SN":"AL0123456789012","Ppv1":"0","Ppv2":"0","Upv1":"7.3","Upv2":"8.3","Ua":"238.8","Ub":"0.0","Uc":"0.0","Fac":"50.02","Ubus":"370","PrealL1":"380","PrealL2":"0.0","PrealL3":"0.0","Tinv":"34","PacL1":"5000","PacL2":"-483","PacL3":"0.0","InvWorkMode":"3","EpvTotal":"35348.5","Einput":"5221.20","Eoutput":"11371.20","Echarge":"9428.4","PmeterL1":"-7","PmeterL2":"0","PmeterL3":"0","PmeterDC":"0","Pbat":"495.5060","SOC":"37.6","BatV":"49.06","BatC":"10.10","FlagBms":"257","BmsWork":"1","Pcharge":"4949","Pdischarge":"4949","BmsRelay":"3","BmsNum":"1","VcellLow":"16911559","VcellHigh":"17108169","TcellLow":"17170460","TcellHigh":"16908317","IdTempelover":"0","IdTempEover":"0","IdTempediffe":"0","IdChargcurre":"0","IdDischcurre":"0","IdCellvolover":"0","IdCellvollower":"0","IdSoclower":"0","IdCellvoldiffe":"0","BatC1":"10.00","BatC2":"0.00","BatC3":"0.00","BatC4":"0.00","BatC5":"0.00","BatC6":"0.00","SOC1":"37.6","SOC2":"0.0","SOC3":"0.0","SOC4":"0.0","SOC5":"0.0","SOC6":"0.0","ErrInv":"0","WarInv":"0","ErrEms":"0","ErrBms":"0","ErrMeter":"0","ErrBackupBox":"0","EGridCharge":"169.5","EDischarge":"9081.1","EmsStatus":"Normal","InvBatV":"49.40","BmsShutdown":"0","BmuRelay":"0","BmsHardVer1":"0", "BmsHardVer2":"0", "BmsHardVer3":"0","DispatchSwitch":"0","Pdispatch":"0", "DispatchSoc":"0", "DispatchMode":"0","PMeterDCL1":"0","PMeterDCL2":"0", "PMeterDCL3":"0","MeterDCUa":"239.2","MeterDCUb":"0.0", "MeterDCUc":"0.0","Eirp":"-36","CSQ":"99,99"}'
    header_and_data = (
        struct.pack(battery.HEADER_FORMAT, 1, 1, 16, 1485)
        + bytes(data, encoding="ascii")
        + bytes((0x57, 0xAC))
    )
    battery.get_command_and_length(header_and_data)
    success = battery.handle_command(header_and_data)
    # success = battery.set_battery_dump(data)
    assert success
    # Add additional assertions for the expected behavior of get_battery_dump
