#!/bin/python
# Sends stuff to the server.

import sys
from socket import *


SERVER_IP: str = 'localhost'
SERVER_PORT: int = 5002


def send_message(sock: socket, message: str) -> str:
    sock.sendall(bytes(message + "\n", "utf-8"))
    print(f"Sent:     {message}")
    data = str(sock.recv(10000), "utf-8")
    return data


if __name__ == "__main__":
    with socket(AF_INET, SOCK_STREAM) as sock:
        sock.connect((SERVER_IP, SERVER_PORT))

        arg = ' '.join(sys.argv[1:])
        response = send_message(sock, arg)
        print(f"Received: {response}")
