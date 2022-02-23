from contextlib import contextmanager
import os
from socket import create_connection
from ssl import SSLContext, PROTOCOL_TLS_CLIENT
import sys


hostname='example.org'
ip = '127.0.0.1'
port = 8443
context = SSLContext(PROTOCOL_TLS_CLIENT)

if '--with-ca' in sys.argv:
    CERT_FILE=f'ca/rootCA.crt'
else:
    CERT_FILE='cert.pem'

context.load_verify_locations(CERT_FILE)

print(f'Connect to {ip}:{port}')
print(f'  hostname {hostname}')
if '--no-ssl' in sys.argv:
    print(f'  without SSL')
else:
    print(f'  with SSL cert {CERT_FILE}')


@contextmanager
def wrap_socket(clientsocket):
    if '--no-ssl' in sys.argv:
        yield clientsocket
    else:
        with context.wrap_socket(clientsocket, server_hostname=hostname) as tls:
            print(f'Using {tls.version()}\n')
            yield tls


with create_connection((ip, port)) as client:
    with wrap_socket(client) as sock:
        sock.sendall(b'Hello, world')

        data = sock.recv(1024)
        print(f'Server says: {data}')
