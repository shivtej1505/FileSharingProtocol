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
    #host = "www.rentooz.com"
except socket.gaierror:
    print 'Hostname could not be resolved.Exiting'
    sys.exit()

try:
    #print (host_ip, port)
    client_socket.connect((host, port))
except Exception, e:
    print "Error: " + str(e)
    sys.exit()

print 'Connected to ' + host

while True:
    try:
        message = raw_input()
        client_socket.sendall(message)
        data = client_socket.recv(1024)
        print data
    except KeyboardInterrupt:
        break
    except socket.error, e:
        print e
        break

client_socket.close()
