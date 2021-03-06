#!/usr/bin/python
import socket
import sys
import os
import stat
import hashlib
import readline
from globals import *

try:
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
except socket.error, msg:
    print 'Error: ' + str(socket.error) + "\n" + str(msg)
    sys.exit()

PORT = 3500
UDP_PORT = 15462
UDP_IP = "127.0.0.1"

client_udp_socket.bind((UDP_IP, UDP_PORT))

while True:
    try:
        download_directory = raw_input("Enter full path of directory in which you want to save downloaded files: ")
        dir_stat = os.stat(download_directory)
        #print dir_stat
    except OSError:
        print "No such directory"
        continue
    except KeyboardInterrupt:
        print "exiting"
        sys.exit()

    if stat.S_ISDIR(dir_stat.st_mode):
        if os.access(download_directory, os.R_OK) and os.access(download_directory, os.W_OK):
            print "Ok, directory is readable and writable"
            break
        else:
            print "Not enough permission.Try again"
            continue
    else:
        print "No such directory"
        continue

print DOWNLOAD_DIRECTORY + ": " + download_directory

def get_response_header():
    response_protocol = client_socket.recv(7)
    #print response_protocol
    response_protocol_attrib = client_socket.recv(64)
    #print response_method
    response_method = response_protocol_attrib[:4]
    response_length = int(response_protocol_attrib[4:])
    #print response_length
    return (response_protocol, response_method, response_length)
try:
    #host_ip = socket.gethostbyname(host)
    #print host_ip
    HOST = socket.gethostname()
except socket.gaierror:
    print 'Hostname could not be resolved.Exiting'
    sys.exit()

try:
    #print (host_ip, port)
    client_socket.connect((HOST, PORT))
except Exception, e:
    print "Cannot connect to server"
    sys.exit()

print 'Connected to ' + HOST

def get_checksum(data):
    md5 = hashlib.md5()
    md5.update(data)
    return md5.hexdigest()

def get_response_body(response_length):
    chunks = []
    current_size = 0
    while current_size < response_length:
        chunk = client_socket.recv(response_length - current_size)
        chunks.append(chunk)
        current_size += len(chunk)

    return ''.join(chunks)

    """
    response_components = response.split("\n")
    response_header = response_components[0]
    if response_header != RESPONSE_HEADER or len(response_components) < 2:
        print "Invalid response"
        return
    print response_components
    
    response_attrib = response_components[1].split()
    response_method = response_attrib[0]
    response_length = int(response_attrib[1])
    response_body = '\n'.join(response_components[2:])
    print "------------------"
    print response_attrib
    print response_method
    print response_length
    print type(response_body)
    print response_body
    valid_response = response_body[:response_length]
    print valid_response
    print len(valid_response)
    print "------------------"
    return tmp
    chunks = []
    while True:
        chunk = client_socket.recv(1024)
        if chunk[-4:] == "\r\n\r\n":
            chunks.append(chunk[:-4])
            break
        chunks.append(chunk)

    return ''.join(chunks)
    """


def process_response():
    response_protocol, response_method, response_length = get_response_header()
    #print response_protocol, response_method, response_length
    #response_body = get_response_body(response_length)
    #print response_body
    if response_protocol != RESPONSE_HEADER:
        print "Invalid response"
        return
    

    if response_method == RESPONSE_METHOD_QUIT:
        print "Closing connection"
        client_socket.close()
        print "Connection closed.Exiting..."
        sys.exit()

    elif response_method == RESPONSE_METHOD_HELP:
        response_body = get_response_body(response_length)
        print "------------------HELP----------------------"
        print response_body 
        print "------------------HELP----------------------"
        return

    elif response_method == RESPONSE_METHOD_INDEX:
        response_body = get_response_body(response_length)
        print "------------------INDEX----------------------"
        print response_body 
        print "------------------INDEX----------------------"
        return
    
    elif response_method == RESPONSE_METHOD_HASH:
        response_body = get_response_body(response_length)
        print "------------------INDEX----------------------"
        print response_body 
        print "------------------INDEX----------------------"
        return

    elif response_method == RESPONSE_METHOD_DOWNLOAD:
        print "------------------FILE-DOWNLOAD----------------------"
        is_download = raw_input("File size is " + str(response_length) + " Download?[y/N] ")
        if is_download == 'y':
            response_body = get_response_body(response_length)

            file_attib = response_body.split("\t")
            file_name = file_attib[0]
            file_size = file_attib[1]
            file_mtime = file_attib[2]
            file_hash = file_attib[3]
            file_content = ' '.join(file_attib[4:])[1:]
            file_content_hash = get_checksum(file_content)

            print "Filename: " + file_name
            print "Filesize: " + file_size
            print "File last modified time: " + file_mtime
            print "File hash: " + file_hash
            print "File New hash: " + file_content_hash
            print "Saving file..."

            file_obj = open(download_directory + "/" + file_name, 'w')
            file_obj.write(file_content)
            file_obj.close()

            print "File saved successfully."
        else:
            response_body = get_response_body(response_length)
            print "Download canceled"

        print "------------------FILE-DOWNLOAD----------------------"
        return

    elif response_method == RESPONSE_METHOD_DOWNLOAD_UDP:
        print "------------------FILE-DOWNLOAD----------------------"
        chunks = []
        current_size = 0
        while current_size < response_length:
            chunk, addr = client_udp_socket.recvfrom(response_length - current_size)
            chunks.append(chunk)
            current_size += len(chunk)
        
        response_body = ''.join(chunks)

        file_attib = response_body.split("\t")
        file_name = file_attib[0]
        file_size = file_attib[1]
        file_mtime = file_attib[2]
        file_hash = file_attib[3]
        file_content = ' '.join(file_attib[4:])[1:]
        file_content_hash = get_checksum(file_content)

        print "Filename: " + file_name
        print "Filesize: " + file_size
        print "File last modified time: " + file_mtime
        print "File hash: " + file_hash
        print "File New hash: " + file_content_hash
        print "Saving file..."

        file_obj = open(download_directory + "/" + file_name, 'w')
        file_obj.write(file_content)
        file_obj.close()

        print "------------------FILE-DOWNLOAD----------------------"

    elif response_method == RESPONSE_METHOD_ERROR:
        response_body = get_response_body(response_length)
        print "------------------ERROR----------------------"
        print response_body 
        print "------------------ERROR----------------------"
        return
    
    else:
        response_body = get_response_body(response_length)
        print "---------------- <server-response> ------------------"
        print response_body
        print "---------------- </server-response> ------------------"
        return

while True:
    try:
        message = raw_input()
        if message:
            client_socket.sendall(message)
        process_response()
    except socket.error, e:
        print "Socket Error: " +  e
        break

client_socket.close()
sys.exit()
