import socket
import time
import sys
from multiprocessing import Process

BUFFER_SIZE = 1024


def get_remote_ip(host):
    try:
        remote_ip = socket.gethostbyname(host)
    except socket.gaierror:
        print('Hostname could not be resolved. Exiting')
        sys.exit()

    return remote_ip


def handle_request(addr, conn, proxy_end):
    print("Connected by", addr)

    full_data = conn.recv(BUFFER_SIZE)
    proxy_end.sendall(full_data)
    reply_data = proxy_end.recv(BUFFER_SIZE)
    conn.send(reply_data)
    proxy_end.shutdown(socket.SHUT_RDWR)
    proxy_end.close()


def main():
    HOST = "localhost"
    PORT = 8081
    EXTERN_HOST = 'www.google.com'
    EXTERN_PORT = 80

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_start:
        print("Starting proxy server")
        proxy_start.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        proxy_start.bind((HOST, PORT))
        proxy_start.listen(1)

        while True:
            conn, addr = proxy_start.accept()

            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_end:
                print("Connecting to Google")
                remote_ip = get_remote_ip(EXTERN_HOST)
                # connect proxy_end
                proxy_end.connect((remote_ip, EXTERN_PORT))

                p = Process(target=handle_request, args=(
                    addr, conn, proxy_end))
                p.daemon = True
                p.start()
                print("Started process ", p)

            conn.close()


if __name__ == "__main__":
    main()
