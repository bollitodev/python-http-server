from collections import deque
from enum import Enum
from typing import Optional


class ChunkReader:
    data: bytes = bytes()
    num_bytes_per_read: int = 4
    pos: int = 0

    def __init__(self, data, num_bytes_per_read) -> None:
        self.data = data.encode()
        self.num_bytes_per_read = num_bytes_per_read

    def read(self, p: list[bytes]) -> int:
        breakpoint()
        if self.pos >= len(self.data):
            return 0
        end_idx = self.pos + self.num_bytes_per_read
        if end_idx > len(self.data):
            end_idx = len(self.data)

        p = [self.data[self.pos : end_idx]]
        n = len(p[0])
        self.pos += n
        return n


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

    def parse(self, data: deque[bytes]) -> int:
        try:
            chunk = data.popleft()
            if not self.state:
                self.state = State.INITIALIZED
            if chunk and self.state is not State.DONE:
                breakpoint()
                decode_data = chunk.decode()
                self._data += decode_data
                return len(chunk)
            elif not chunk:
                self.state = State.DONE
                return 0
        except Exception as e:
            raise ErrorParsingData(f"Error parsing bytes: {e}")
        finally:
            return 0

    def parse_request_line(self) -> int:
        print(f"data {self._data}")
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


def request_from_reader(reader: ChunkReader) -> Request:
    request = Request()
    print(f"state (outside) {request.state}")
    data_bytes: list[bytes] = []
    queue = deque()
    while request.state != State.DONE:
        bytes_read = reader.read(data_bytes)
        queue.append(data_bytes[0])
        print(f"Bytes read: {bytes_read}")
        request.parse(queue)
    request.parse_request_line()
    return request
