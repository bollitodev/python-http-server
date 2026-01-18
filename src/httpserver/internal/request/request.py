import socket
from collections import deque
from enum import Enum
from typing import Optional


class RequestLine:
    http_version: str
    request_target: str
    method: str


class ErrorParsingData(Exception):
    def __init__(self, message) -> None:
        self.message = message


class State(Enum):
    INITIALIZED = 0
    DONE = 1


class Request:
    state: Optional[State] = None
    request_line: RequestLine
    _data: str = ""

    def parse(self, chunk: bytes) -> int:
        try:
            if not chunk:
                self.state = State.DONE
                return 0
            if not self.state:
                self.state = State.INITIALIZED
            if chunk and self.state is not State.DONE:
                decode_data = chunk.decode()
                self._data += decode_data
                return len(chunk)
        except Exception as e:
            raise ErrorParsingData(f"Error parsing bytes: {e}")
        finally:
            return 0

    def parse_request_line(self) -> int:
        if HTTP_SEPARATOR in self._data:
            line = self._data.split(HTTP_SEPARATOR)[0].split(" ")
            if len(line) != 3:
                raise InvalidRequestLine(
                    f"Invalid number of elements in request line {line}"
                )

            rq_line = RequestLine()

            if line[0] not in AVAILABLE_HTTP_METHODS:
                raise ErrorReadingMethod(
                    f"Error reading method from request: {line[0]}"
                )

            rq_line.method = line[0]
            rq_line.request_target = line[1]
            http_name, http_version = line[2].split("/")

            if "HTTP" not in http_name:
                raise HttpVersionNotSupported(f"HTTP {http_name} name not suppoted")
            if http_version != SUPPORT_HTTP_VERSION:
                raise HttpVersionNotSupported(
                    f"HTTP {http_version} version not suppoted"
                )

            rq_line.http_version = http_version
            self.request_line = rq_line
            return len(self._data)
        return 0


class ErrorReadingMethod(Exception):
    def __init__(self, message):
        self.message = message


class HttpVersionNotSupported(Exception):
    def __init__(self, message) -> None:
        self.message = message


class InvalidRequestLine(Exception):
    def __init__(self, message) -> None:
        self.message = message


HTTP_SEPARATOR = "\r\n"
SUPPORT_HTTP_VERSION = "1.1"
AVAILABLE_HTTP_METHODS = ["GET", "POST", "PUT", "PATCH"]


def request_from_reader(reader) -> Request:
    request = Request()
    while request.state != State.DONE:
        data = reader.recv(8)
        request.parse(data)
    request.parse_request_line()
    return request
