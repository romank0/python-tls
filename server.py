import os
from socket import socket, AF_INET, SOCK_STREAM
from ssl import SSLContext, PROTOCOL_TLS_SERVER
import sys
from threading import Thread


hostname = 'example.org'
ip = '127.0.0.1'
port = 8443
context = SSLContext(PROTOCOL_TLS_SERVER)

if '--with-ca' in sys.argv:
    CERT_FILE=f'ca/{hostname}/{hostname}.crt'
    KEY_FILE=f'ca/{hostname}/{hostname}.key'
else:
    CERT_FILE='cert.pem'
    KEY_FILE='key.pem'

context.load_cert_chain(CERT_FILE, KEY_FILE)

print(f'Listening on {ip}:{port}')
print(f'  hostname {hostname}')
print(f'  cert {CERT_FILE}')
print(f'  key {KEY_FILE}')


def handle(connection, address):
    print(f'Connected by {address}\n')

    data = connection.recv(1024)
    print(f'Client Says: {data}')

    connection.sendall(b"You're welcome")


with socket(AF_INET, SOCK_STREAM) as server:
    server.bind((ip, port))
    server.listen(5)
    with context.wrap_socket(server, server_side=True) as tls:
        while True:
            try:
                connection, address = tls.accept()
                Thread(target=handle, args=(connection, address)).run()
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f'Error: {e}')
