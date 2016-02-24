#!/usr/bin/python
import socket
import sys
from globals import *

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

def get_response_header():
    response_protocol = client_socket.recv(7)
    response_protocol_attrib = client_socket.recv(64)
    response_method = response_protocol_attrib[:4]
    response_length = int(response_protocol_attrib[4:])
    #print response_protocol
    #print response_method
    #print response_length
    return (response_protocol, response_method, response_length)

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

            print "Filename: " + file_name
            print "Filesize: " + file_size
            print "File last modified time: " + file_mtime
            print "File hash: " + file_hash
            print "Saving file..."

            file_obj = open(file_name, 'w')
            file_obj.write(file_content)
            file_obj.close()

            print "File saved successfully."
        else:
            response_body = get_response_body(response_length)
            print "Download canceled"

        print "------------------FILE-DOWNLOAD----------------------"
        return
    
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
