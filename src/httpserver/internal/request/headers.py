CRLF = b"\r\n"

class Headers():

    Headers = {}


    @staticmethod
    def parse_header(field_line: bytes)->tuple[str, str]:
        parts = field_line.split(b":", 1)
        if len(parts) != 2:
            raise InvalidHeaderFormat(f"Malformmed field line: {field_line}")
        name = parts[0]
        value = parts[1].strip()
        if name.endswith(b" "):
            raise InvalidHeaderFormat(f"Extra space between name field: '{name}' ")
        return name.decode(), value.decode() 


    def parse(self, data: bytes):
        read = 0
        done = False
        while True:
            idx = data[read:].index(CRLF)
            if idx == -1:
                break
            if idx == 0:
                done = True
                break
            name, value= self.parse_header(data[read:read+idx])
            read += idx + len(CRLF) 
            self.Headers[name] = value
        
        return read, done 


class InvalidHeaderFormat(Exception):
    def __init__(self, message) -> None:
        self.message = message
