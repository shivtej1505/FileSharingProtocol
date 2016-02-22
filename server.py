#!/usr/bin/python
import socket
import sys

HOST = ''
PORT = 3500

INVALID_COMMAND = "Invalid command"

COMMAND_HELP = "help"  # help command
COMMAND_HELP_FLAG_1 = "commands" # get list of commands available
COMMAND_HELP_FLAG_2 = "IndexGet" # get list of shared files
COMMAND_HELP_FLAG_3 = "FileHash"


COMMAND_INDEX_GET = "IndexGet"
COMMAND_INDEX_GET_FLAG_1 = "shortlist"
COMMAND_INDEX_GET_FLAG_2 = "longlist"
COMMAND_INDEX_GET_FLAG_3 = "regex"


try:
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error, msg:
    print 'Error creating socket: ' + str(msg) + '.\nError: ' + socket.error
    sys.exit()

server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)


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


def run_command(request):
    # is valid command
    request_components = request.split()
    print request_components
    if len(request_components) > 2 or len(request_components) <= 0:
        print "Invalid request by client"
        conn.sendall(INVALID_COMMAND)
        return

    command = request_components[0]
    flag = None
    if len(request_components) == 2:
        flag = request_components[1]
    
    # identifying the command
    if command == COMMAND_HELP:
        if flag == None or flag == COMMAND_HELP_FLAG_1:
            help_string = "The help command\nAvailable commands:\n"
            help_string += COMMAND_HELP + "\n"
            help_string += COMMAND_INDEX_GET
            conn.sendall(help_string)

        elif flag == COMMAND_HELP_FLAG_2:
            help_string = "Get list of shared files, which you can download."
            conn.sendall(help_string)

        elif flag == COMMAND_HELP_FLAG_3:
            help_string = "Donno"
            conn.sendall(help_string)

    elif command == "IndexGet":
        print "Client requested for list of shared files"
        print "sending list..."
        #if flag == COMMAND_INDEX_GET_FLAG_1:
        conn.sendall("LOL")
        print "list sent successfully"
    elif command == "quit":
        print "closing connection"
        conn.sendall("quit")
        conn.close()
        print "connection closed.Exiting..."
        sys.exit()

        

while True:
    try:
        data = conn.recv(1024)
        if data:
            print "Command from " + addr[0] + ":" + data
            run_command(data)
    except KeyboardInterrupt:
        print "exiting"
        break
    except Exception, e:
        print "An error occured"
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
