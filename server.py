#!/usr/bin/python
import socket
import sys
import os
import stat
import time

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


COMMAND_FILE_HASH = "FileHash"
COMMAND_FILE_HASH_FLAG_1 = "verify"
COMMAND_FILE_HASH_FLAG_2 = "checkall"


COMMAND_QUIT = "quit"

SHARED_DIRECTORY = "SHARED DIRECTORY"

FILE_TYPE_UNKNOWN = "Unknown"

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

while True:
    shared_directory = raw_input("Enter full path of shared directory: ")
    try:
        dir_stat = os.stat(shared_directory)
        print dir_stat
    except OSError:
        print "No such directory"
        continue

    if stat.S_ISDIR(dir_stat.st_mode):
        if os.access(shared_directory, os.R_OK) and os.access(shared_directory, os.W_OK):
            print "Ok, directory is readable and writable"
            break
        else:
            print "Not enough permission.Try again"
            continue
    else:
        print "No such directory"
        continue

print SHARED_DIRECTORY + ": " + shared_directory

server_socket.listen(5)

print 'Listing to incoming connections'

conn, addr = server_socket.accept()

print 'Connected to ' + str(addr[0]) + ":" + str(addr[1])


def send_to_client(data):
    DATALEN = len(data)
    total_sent = 0
    while total_sent < DATALEN:
        sent = conn.send(data[total_sent:])
        if sent == 0:
            raise RunTimeError("Socket connection broken")
        total_sent += sent


def receive_from_client():
    chunks = []
    bytes_received = 0
    DATALEN = 1024
    while bytes_received < DATALEN:
        chunk = conn.recv(1024)
        if chunk == '':
            raise RunTimeError("Socket connection broken")
        chunks.append(chunk)
        bytes_received += 1024
    return ''.join(chunks)

def run_command(request):
    # is valid command
    request_components = request.split()
    #print request_components
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
        # help command
        if flag == None or flag == COMMAND_HELP_FLAG_1:
            help_string = "The help command\nAvailable commands:\n"
            help_string += COMMAND_HELP + "\n"
            help_string += COMMAND_INDEX_GET + "\n"
            help_string += COMMAND_FILE_HASH
            conn.sendall(help_string)

        elif flag == COMMAND_HELP_FLAG_2:
            help_string = "Get list of shared files, which you can download.\n"
            help_string += "Flags available:\n"
            help_string += COMMAND_INDEX_GET_FLAG_1 + "\n"
            help_string += COMMAND_INDEX_GET_FLAG_2 + "\n"
            help_string += COMMAND_INDEX_GET_FLAG_3
            conn.sendall(help_string)

        elif flag == COMMAND_HELP_FLAG_3:
            help_string = "Donno\n"
            help_string += "Flags available:\n"
            help_string += COMMAND_FILE_HASH_FLAG_1 + "\n"
            help_string += COMMAND_FILE_HASH_FLAG_2 + "\n"
            conn.sendall(help_string)

    elif command == COMMAND_INDEX_GET:
        # IndexGet command
        print "Client requested for list of shared files"
        print "sending list..."
        if flag == COMMAND_INDEX_GET_FLAG_1:
            response = "Filename\t" + "Size\t\t" + "Date\t\t" + "\t\tType\n"
            files = os.listdir(shared_directory)
            print files

            for a_file in files:
                file_stat = os.stat(shared_directory + "/" + a_file)
                file_size = str(file_stat.st_size)
                file_ctime = str(time.ctime(file_stat.st_ctime))
                file_comp = a_file.split('.')
                file_type = FILE_TYPE_UNKNOWN

                if len(file_comp) == 2:
                    file_type = file_comp[1]

                response += a_file + "\t\t" + file_size + " bytes\t"
                response +=  file_ctime + "\t" + file_type + "\n"

            send_to_client(response)

        elif flag == COMMAND_INDEX_GET_FLAG_2:
            send_to_client("Flag 2")
        elif flag == COMMAND_INDEX_GET_FLAG_3:
            send_to_client("Flag 3")
        else:
            send_to_client(INVALID_COMMAND)
            print INVALID_COMMAND
            return
        print "list sent successfully"
        return


    elif command == COMMAND_QUIT:
        # Quit command
        print "closing connection"
        conn.sendall("quit")
        conn.close()
        print "connection closed.Exiting..."
        sys.exit()

    else:
        # Invalid command
        send_to_client(INVALID_COMMAND)
        print INVALID_COMMAND


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
        send_to_client(COMMAND_QUIT)
        print e
        break

conn.close()
sys.exit()
