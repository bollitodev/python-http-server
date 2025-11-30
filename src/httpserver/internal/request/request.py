from io import StringIO


class RequestLine:
    http_version: str
    request_target: str
    method: str

class Request:
    request_line: RequestLine
    def __init__(self, request_line) -> None:
       self.request_line = request_line

class ErrorReadingMethod(Exception):
    def __init__(self, message):
        self.message = message

class HttpVersionNotSupported(Exception):
    def __init__(self, message) -> None:
        self.message = message

class InvalidRequestLine(Exception):
    def __init__(self, message) -> None:
        self.message = message


HTTP_SEPARATOR="\r\n"
SUPPORT_HTTP_VERSION = "1.1"
AVAILABLE_HTTP_METHODS = ["GET", "POST", "PUT", "PATCH"]


def parse_request_line(request_line:str)->Request:
    line = request_line.split(HTTP_SEPARATOR)[0].split(" ")
    if len(line) != 3:
        raise InvalidRequestLine(f"Invalid number of elements in request line {line}")

    rq_line = RequestLine()

    if line[0] not in AVAILABLE_HTTP_METHODS:
        raise ErrorReadingMethod(f"Error reading method from request: {line[0]}")

    rq_line.method = line[0]
    rq_line.request_target = line[1]
    http_name, http_version = line[2].split("/")


    if "HTTP" not in http_name:
        raise HttpVersionNotSupported(f"HTTP {http_name} name not suppoted")
    if http_version != SUPPORT_HTTP_VERSION:
        raise HttpVersionNotSupported(f"HTTP {http_version} version not suppoted")

    rq_line.http_version = http_version

    return Request(request_line=rq_line)


def request_from_reader(reader:StringIO)->Request:
    return parse_request_line(reader.read())
