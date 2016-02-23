#!/usr/bin/python
import socket
import sys

try:
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error, msg:
    print 'Error: ' + str(socket.error) + "\n" + str(msg)
    sys.exit()

port = 3500

try:
    #host_ip = socket.gethostbyname(host)
    #print host_ip
    host = socket.gethostname()
except socket.gaierror:
    print 'Hostname could not be resolved.Exiting'
    sys.exit()

try:
    #print (host_ip, port)
    client_socket.connect((host, port))
except Exception, e:
    print "Cannot connect to server"
    sys.exit()

print 'Connected to ' + host

def process_response(response):
    if response == "quit":
        print "Closing connection"
        client_socket.close()
        print "Connection closed.Exiting..."
        sys.exit()
    else:
        print "---------------- <server-response> ------------------"
        print response
        print "---------------- </server-response> ------------------"


while True:
    try:
        message = raw_input()
        if message:
            client_socket.sendall(message)
        response = client_socket.recv(1024)
        if response:
            process_response(response)
    except socket.error, e:
        print "Socket Error: " +  e
        break

client_socket.close()
sys.exit()
