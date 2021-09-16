import socket
from multiprocessing import Pool

HOST = "localhost"
PORT = 8081
BUFFER_SIZE = 1024

payload = f'GET / HTTP/1.0\r\nHost: www.google.com\r\n\r\n'


def connect(addr):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(addr)
        s.sendall(payload.encode())
        s.shutdown(socket.SHUT_WR)

        full_data = s.recv(BUFFER_SIZE)
        print(f"received connection {addr}\n")
        print(full_data)

    except Exception as e:
        print(e)
    finally:
        # always close at the end!
        s.close()


def main():
    address = [(HOST, PORT)]
    # establist 10 different connections
    with Pool() as p:
        p.map(connect, address * 10)


if __name__ == "__main__":
    main()
