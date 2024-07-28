#!/bin/python
# Sends stuff to the server.

import sys
from socket import *


SERVER_IP = '10.10.11.18'
SERVER_PORT = 5002


def send_message(sock, message):
    sock.sendall(bytes(message + "\n", "utf-8"))
    print("Sent:     {message}".format(message=message))
    data = str(sock.recv(10000), "utf-8")
    return data


if __name__ == "__main__":
    with socket(AF_INET, SOCK_STREAM) as sock:
        sock.connect((SERVER_IP, SERVER_PORT))

        arg = ' '.join(sys.argv[1:])
        response = send_message(sock, arg)
        print("Received: {response}".format(response=response))
