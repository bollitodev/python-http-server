WHITE_SPACE = " "
CRLF = "\r\n"
HOST_KEYNAME = "Host:"

class Headers():

    Host = ""
    Headers = {}
    _is_done: bool = False
    _counter_char: int = 0
    _last_char = ""


    def parse(self, data: bytes):
        for i in data.decode():
            if CRLF == self._last_char+i:
                self._is_done = True
                break
            if i is WHITE_SPACE and self._counter_char<1:
                continue
            if self._counter_char<len(HOST_KEYNAME):
                if i != HOST_KEYNAME[self._counter_char]:
                    raise InvalidHostFormat(f"Invalid header format: '{self.Host}'") 
                self._counter_char+=1
                self._is_done = True
                continue
            if i is WHITE_SPACE or i in CRLF:
                continue
            self.Host += i
            self._last_char = i
        
        
        if not self._is_done:
            raise InvalidHostFormat(f"Data is empty: '{self.Host}'")
        self.Headers['Host'] = self.Host
        return len(data)-2, self._is_done



class InvalidHostFormat(Exception):
    def __init__(self, message) -> None:
        self.message = message
