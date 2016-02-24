#!/usr/bin/python
import socket
import sys
import os
import stat
import time
from datetime import datetime
from globals import *

HOST = ''
PORT = 3500

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


def send_to_client(data, method_name):
    conn.send(RESPONSE_HEADER + "\n")
    conn.send(method_name + "\n")
    DATALEN = len(data)
    total_sent = 0
    while total_sent < DATALEN:
        sent = conn.send(data[total_sent:])
        if sent == 0:
            raise RunTimeError("Socket connection broken")
        total_sent += sent

    conn.send(RESPONSE_FOOTER)


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

def invalid_command():
    print "Invalid command issued by client"
    send_to_client(INVALID_COMMAND, RESPONSE_METHOD_ERROR)
    return


def is_file_in_shared_folder(file_name):
    return True

def run_command(request):
    # is valid command
    request_components = request.split()
    #print request_components
    if len(request_components) <= 0:
        invalid_command()
        return

    command = request_components[0]
    flag = None
    if len(request_components) >= 2:
        flag = request_components[1]
    
    # identifying the command
    if command == COMMAND_HELP:
        # help command
        if flag == None or flag == COMMAND_HELP_FLAG_1:
            help_string = "The help command\nAvailable commands:\n"
            help_string += COMMAND_HELP + "\n"
            help_string += COMMAND_INDEX_GET + "\n"
            help_string += COMMAND_FILE_HASH + "\n"
            help_string += COMMAND_FILE_DOWNLOAD
            send_to_client(help_string, RESPONSE_METHOD_HELP)

        elif flag == COMMAND_HELP_FLAG_2:
            help_string = "Get list of shared files, which you can download.\n"
            help_string += "Flags available:\n"
            help_string += COMMAND_INDEX_GET_FLAG_1 + "\n"
            help_string += COMMAND_INDEX_GET_FLAG_2 + "\n"
            help_string += COMMAND_INDEX_GET_FLAG_3
            send_to_client(help_string, RESPONSE_METHOD_HELP)

        elif flag == COMMAND_HELP_FLAG_3:
            help_string = "Donno\n"
            help_string += "Flags available:\n"
            help_string += COMMAND_FILE_HASH_FLAG_1 + "\n"
            help_string += COMMAND_FILE_HASH_FLAG_2 + "\n"
            send_to_client(help_string, RESPONSE_METHOD_HELP)

        elif flag == COMMAND_HELP_FLAG_4:
            help_string = "Download files from shared folder\n"
            help_string += "Flags available:\n"
            help_string += COMMAND_FILE_DOWNLOAD_FLAG_1 + "\n"
            help_string += COMMAND_FILE_DOWNLOAD_FLAG_2 + "\n"
            send_to_client(help_string, RESPONSE_METHOD_HELP)

    elif command == COMMAND_INDEX_GET:
        # IndexGet command
        print "Client requested for list of shared files"
        print "sending list..."
        if flag == COMMAND_INDEX_GET_FLAG_1:
            if len(request_components) < 4:
                invalid_command()
                return
            try:
                start_date = datetime.strptime(request_components[2], "%d-%m-%Y")
                end_date = datetime.strptime(request_components[3], "%d-%m-%Y")
            except TypeError, e:
                print e
                return
            print start_date
            print end_date

            response = "Filename\t" + "Size\t\t" + "Date\t\t" + "\t\tType\n"
            files = os.listdir(shared_directory)
            print files

            for a_file in files:
                file_stat = os.stat(shared_directory + "/" + a_file)
                file_size = str(file_stat.st_size)
                file_ctime = str(time.ctime(file_stat.st_ctime))
                file_date = time.strftime("%d-%m-%Y", time.localtime(file_stat.st_ctime))
                file_cdate = datetime.strptime(file_date, "%d-%m-%Y")
                file_comp = a_file.split('.')
                file_type = FILE_TYPE_UNKNOWN

                if len(file_comp) == 2:
                    file_type = file_comp[1]

                if start_date <= file_cdate and file_cdate <= end_date:
                    response += a_file + "\t\t" + file_size + " bytes\t"
                    response +=  file_ctime + "\t" + file_type + "\n"
                
            send_to_client(response, RESPONSE_METHOD_INDEX)

        elif flag == COMMAND_INDEX_GET_FLAG_2:
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

            send_to_client(response, RESPONSE_METHOD_INDEX)

        elif flag == COMMAND_INDEX_GET_FLAG_3:
            send_to_client(response, RESPONSE_METHOD_INDEX)

        else:
            invalid_command()

        print "list sent successfully"
        return

    elif command == COMMAND_FILE_HASH:
        send_to_client(COMMAND_FILE_HASH, RESPONSE_METHOD_HASH)

    elif command == COMMAND_FILE_DOWNLOAD:
        if len(request_components) < 3:
            invalid_command()
            return
        file_name = request_components[2]
        print file_name
        try:
            file_stat = os.stat(shared_directory + "/" + file_name)
        except OSError:
            invalid_command()
            return
        print file_stat
        if is_file_in_shared_folder(file_name):
            print "Sending file..."
            send_to_client(COMMAND_FILE_DOWNLOAD, RESPONSE_METHOD_DOWNLOAD)
        else:
            send_to_client("No such file", RESPONSE_METHOD_ERROR)

    elif command == COMMAND_QUIT:
        # Quit command
        print "closing connection"
        send_to_client(COMMAND_QUIT, RESPONSE_METHOD_QUIT)
        conn.close()
        print "connection closed.Exiting..."
        sys.exit()

    else:
        # Invalid command
        invalid_command()


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
        send_to_client(COMMAND_QUIT, RESPONSE_METHOD_QUIT)
        print e
        break

conn.close()
sys.exit()
