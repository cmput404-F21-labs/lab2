#!/usr/bin/env python3
import socket
import time
import sys

# define address & buffer size
HOST = ""
PORT = 8001
BUFFER_SIZE = 1024


def get_remote_ip(host):
    try:
        remote_ip = socket.gethostbyname(host)
    except socket.gaierror:
        print('Hostname could not be resolved. Exiting')
        sys.exit()

    return remote_ip


def main():
    extern_host = 'www.google.com'
    extern_port = 80

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_start:
        print("Starting proxy server")
        proxy_start.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        proxy_start.bind((HOST, PORT))
        proxy_start.listen(1)

        # continuously listen for connections
        while True:
            conn, addr = proxy_start.accept()
            print("Connected by", addr)

            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_end:
                print("Connecting to Google")
                remote_ip = get_remote_ip(extern_host)

                # connect proxy_end
                proxy_end.connect((remote_ip, extern_port))

                # send data
                data = conn.recv(BUFFER_SIZE)
                proxy_end.sendall(data)
                reply_data = proxy_end.recv(BUFFER_SIZE)
                print(f"\nSending recieved data {data} to client")
                # send data back
                conn.send(reply_data)

            conn.close()


if __name__ == "__main__":
    main()
