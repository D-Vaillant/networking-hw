#!/bin/python
# Receives sent files.
import os
import socket
import socketserver

SERVER_PORT = 5002
CODE = "SECRET"

class FileHandler(socketserver.StreamRequestHandler):
    def handle(self):
        print("Connected to {}.".format(self.client_address[0]))

        header = self.request.recv(120)
        filename = header[:100].decode().strip()
        expected_size = header[100:].decode().strip()
        expected_size = int(expected_size)

        print("Receiving file: {filename}".format(filename=filename))
        print("Expected size: {} bytes".format(expected_size))
        
        with open(filename, 'wb') as file:
            received_size = 0
            while received_size < expected_size:
                data = self.request.recv(min(1024, expected_size - received_size))
                if not data:
                    break
                file.write(data)
                received_size += len(data)
        
        actual_size = os.path.getsize(filename)
        if actual_size == expected_size:
            print("File received successfully: {}".format(filename))
            print("File size: {} bytes".format(actual_size))
        else:
            print("Error: File size mismatch. Expected {} bytes, got {} bytes.".format(expected_size, actual_size))


if __name__ == "__main__":
    server = socketserver.TCPServer(('', SERVER_PORT), FileHandler)
    server.serve_forever()
