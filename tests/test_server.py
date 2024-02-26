from unittest.mock import MagicMock

import pytest
import socket
from unittest.mock import patch

from src.server.server import BatteryTCPHandler


def test_timeout_exception():
    with patch("socket.socket") as mock_socket:
        # Configure the mock socket to raise a timeout exception when recv is called
        mock_socket.recv.side_effect = socket.timeout

        # Call the function that's supposed to handle the timeout exception
        with pytest.raises(socket.timeout):
            data = mock_socket.recv(1024)


@pytest.fixture(name="handler")
def fixture_handler():
    request = MagicMock()
    client_address = ("localhost", 12345)
    server = MagicMock()
    return BatteryTCPHandler(request, client_address, server)


def test_handle_no_data(handler):
    handler.request.recv.return_value = b""
    handler.handle()
    assert handler.request.sendall.called == ValueError


def test_handle_invalid_header_size(handler):
    handler.request.recv.return_value = b"123"
    handler.handle()
    assert not handler.request.sendall.called
    assert handler.log_error.called
    handler.log_error.assert_called_with(
        "Error in Header Size. Received Data Length: 3, Expected Minimum: {header_size}",
        len(data),
        this_battery.get_header_size(),
        exc_info=True,
    )


def test_handle_valid_data(handler):
    handler.request.recv.return_value = b"1234567890"
    # Add assertions for this test


def test_get_extra_data(handler):
    battery = MagicMock()
    battery.get_header_size.return_value = 10
    battery.CHECKSUM_SIZE = 2
    data = b"1234567890"
    length = 20
    handler.request.recv.return_value = b"1234567890"
    result = handler.get_extra_data(battery, data, length)
    assert len(result) == length
    assert result == data + handler.request.recv.return_value
