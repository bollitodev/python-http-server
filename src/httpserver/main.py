import socket
from internal.request.request import (
    request_from_reader,
)


def main()->None:
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("127.0.0.1", 42068))
    server.listen(5)
    listener, _ = server.accept()
    r = request_from_reader(listener)
    print("Request line:")
    print("- Method: ", r.request_line.method)
    print("- Target: ", r.request_line.request_target)
    print("- Version: ", r.request_line.http_version)
    server.close()

if __name__ == "__main__":
    main()
