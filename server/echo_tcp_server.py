#!/bin/python
# Receives input from a socket. If secret code is found, respond with number of digits.
# Else, respond with "Secret not found."
import re
import socket
import socketserver

SERVER_PORT = 5002
CODE = "SECRET"

class SecretCodeHandler(socketserver.StreamRequestHandler):
    def handle(self):
        self.data =  self.rfile.readline().strip().decode('utf-8')
        print("{} wrote: {}".format(self.client_address[0],
                                    self.data))
        if CODE in self.data:
            digits, digits_count = count_digits(self.data)
            response = "Digits: {} Count: {}".format(digits, digits_count)
        else:
            response = "Secret code not found."
        self.wfile.write(response.encode('utf-8'))


def count_digits(input):
    digits_pattern = re.compile(r'[^0-9]')
    digits = digits_pattern.sub('', input)
    return digits, len(digits)


if __name__ == "__main__":
    with socketserver.TCPServer(('', SERVER_PORT), SecretCodeHandler) as server:
        server.serve_forever()
