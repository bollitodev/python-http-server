from typing import Any, Generator
import queue
from threading import Thread
import socket


def read_in_chunks(file_object:socket.socket, chunk_size:int=8)->Generator[bytes, Any, Any]:
    while True:
        data = file_object.recv(chunk_size)
        if not data:
            break
        yield data

def read_lines(conn:socket.socket, q:queue.Queue)->None:
    current_line: bytes = bytes()
    for chunk in read_in_chunks(conn):
        parts = chunk.split(b'\n')
        current_line += parts[0]
        if len(parts) > 1:
            q.put(current_line)
            current_line = parts[1] 
    q.put(current_line)
    q.put(None)


def main()->None:
    messages = queue.Queue()
    thread = None
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("127.0.0.1", 42068))
    server.listen(5)
    listener, _ = server.accept()

    thread = Thread(target=read_lines, args = (listener, messages))
    thread.start()
    

    line = messages.get()
    encoding = "utf-8"
    while line:
        print(f"{line.decode(encoding)}")
        line = messages.get()

    thread.join()
    server.close()

if __name__ == "__main__":
    main()
