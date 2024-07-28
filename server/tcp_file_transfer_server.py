#!/bin/python
# Receives sent files.
import os
import socket
import socketserver

SERVER_PORT: int = 5002
CODE: str = "SECRET"

class FileHandler(socketserver.StreamRequestHandler):
    def handle(self):
        print(f"Connected to {self.client_address[0]}")

        header = self.request.recv(1024).decode().strip()
        filename, expected_size = header.split('\t')
        expected_size = int(expected_size)

        print(f"Receiving file: {filename}")
        print(f"Expected size: {expected_size} bytes")
        
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
            print(f"File received successfully: {filename}")
            print(f"File size: {actual_size} bytes")
        else:
            print(f"Error: File size mismatch. Expected {expected_size} bytes, got {actual_size} bytes.")


if __name__ == "__main__":
    with socketserver.TCPServer(('', SERVER_PORT), FileHandler) as server:
        server.serve_forever()
