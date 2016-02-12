#!/usr/bin/python
import socket
import sys

try:
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error, msg:
    print 'Error creating socket: ' + str(msg) + '.\nError: ' + socket.error
    sys.exit()

server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

HOST = ''
PORT = 3500

try:
    server_socket.bind((HOST, PORT))
except socket.error, msg:
    print 'Bind failed. Error Code: ' + str(msg)
    sys.exit()

print 'Socket bind complete'

server_socket.listen(5)
print 'Listing to incoming connections'

conn, addr = server_socket.accept()

print 'Connected to ' + str(addr[0]) + ":" + str(addr[1])

while True:
    try:
        data = conn.recv(1024)
        print data
        msg = raw_input()
        conn.sendall(msg)
    except KeyboardInterrupt:
        print "exiting"
        break
    except Exception, e:
        print e
        break

conn.close()
sys.exit()

'''
while True:
    try:
        client_socket, addr = server_socket.accept()

        print("Connection from %s, %s" % (str(addr), str(client_socket)) )
        #current_time = time.ctime(time.time()) + "\r\n"
        data = raw_input()
        #client_socket.send(current_time.encode('ascii'))
        client_socket.send(data)
    except:
        client_socket.close()
        break
'''
