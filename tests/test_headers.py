from src.httpserver.internal.request.headers import InvalidHeaderFormat 
from src.httpserver.internal.request.headers import Headers


def test_valid_single_header():
    try: 
        headers = Headers()
        data = b'Host: localhost:42069\r\n fooFoo: sdasdas\r\n\r\n'
        n, done = headers.parse(data)
        assert headers.Headers is not None
        assert "localhost:42069" == headers.Headers["Host"]
        assert "sdasdas" == headers.Headers[" fooFoo"]
        assert 41 == n
        assert done
    except Exception as error:
        assert False, f"It should not had any error {error}"


def test_invalid_spacing_header():
    try:
        headers = Headers()
        data = b"       Host : localhost:42069       \r\n\r\n"
        n, done = headers.parse(data)
        assert False, "It should return a InvalidHeaderFormat Exception"
    except InvalidHeaderFormat:
        assert True
