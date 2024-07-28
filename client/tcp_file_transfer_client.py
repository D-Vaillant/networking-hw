# Sents text files.
import sys
from pathlib import Path
from socket import *


SERVER_IP: str = 'localhost'
SERVER_PORT: int = 5002


def send_file(sock: socket, text_file: Path):
    filename = text_file.name
    filesize = text_file.stat().st_size
    header = f"{filename}\t{filesize}\n"
    sock.send(bytes(header, 'utf-8'))

    with text_file.open('rb') as filebytes:
        sock.sendfile(filebytes, 0, filesize)

    print(f"Header: {header}")


if __name__ == "__main__":
    try:
        file_to_send = Path(sys.argv[1])
    except IndexError:
        print("No file specified.")

    if not file_to_send.exists():
        print("File doesn't exist.")
        sys.exit(1)

    with socket(AF_INET, SOCK_STREAM) as sock:
        sock.connect((SERVER_IP, SERVER_PORT))
        send_file(sock, file_to_send)

