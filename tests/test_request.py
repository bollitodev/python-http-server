from src.httpserver.internal.request.request import (
    InvalidRequestLine,
    request_from_reader,
)


class ChunkReader:
    data: bytes = bytes()
    num_bytes_per_read: int = 4
    pos: int = 0

    def __init__(self, data, num_bytes_per_read) -> None:
        self.data = data.encode()
        self.num_bytes_per_read = num_bytes_per_read

    def recv(self, byte_size) -> bytes:
        if self.pos >= len(self.data):
            return b""
        end_idx = self.pos + self.num_bytes_per_read
        if end_idx > len(self.data):
            end_idx = len(self.data)

        chunk = self.data[self.pos : end_idx]
        n = len(chunk)
        self.pos += n
        return chunk


def test_good_resquest_line_parse():
    try:
        reader = ChunkReader(
            data="GET / HTTP/1.1\r\nHost: localhost:42069\r\nUser-Agent: curl/7.81.0\r\nAccept: */*\r\n\r\n",
            num_bytes_per_read=3,
        )

        r = request_from_reader(reader)
        assert "GET" == r.request_line.method
        assert "/" == r.request_line.request_target
        assert "1.1" == r.request_line.http_version
    except Exception as exception:
        assert False, f"Should not fail with except: {exception}"


def test_good_resquest_line_with_path_parse():
    try:
        r = request_from_reader(
            ChunkReader(
                data="GET /coffee HTTP/1.1\r\nHost: localhost:42069\r\nUser-Agent: curl/7.81.0\r\nAccept: */*\r\n\r\n",
                num_bytes_per_read=3
            )
        )
        assert "GET" == r.request_line.method
        assert "/coffee" == r.request_line.request_target
        assert "1.1" == r.request_line.http_version
    except Exception as exception:
        assert False, f"Should not fail with except: {exception}"


def test_invalid_number_parts_in_request_line():
    try:
        request_from_reader(
            ChunkReader(
                data="/coffee HTTP/1.1\r\nHost: localhost:42069\r\nUser-Agent: curl/7.81.0\r\nAccept: */*\r\n\r\n",
                num_bytes_per_read=3
            )
        )
        assert False, "Should return an InvalidRequestLine exception"
    except InvalidRequestLine:
        assert True
