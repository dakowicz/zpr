#!/usr/bin/python
import os.path
import sys
sys.path.append(os.path.pardir)
import threading
import socket
import json
from utils.message import Message

playing = False


class Handler(threading.Thread):
    def __init__(self, server_socket, size):
        threading.Thread.__init__(self)
        self.server_socket = server_socket
        self.size = size

    def run(self):
        while True:
            try:
                response = json.loads(self.server_socket.recv(self.size))
            except ValueError:
                print 'ValueError'
            print str(response['players_number'])
            i = 0
            while i < response['players_number']:
                print response[str(i)]
                i += 1
            print response['table_card_0'] + ' ' + response['table_card_1'] + ' ' + response['table_card_2'] + ' ' + response['table_card_3'] + ' ' + response['table_card_4']
            print str(response['win']) + ' ' + str(response['draw']) + ' ' + str(response['loss'])
            if 'dealer' in response:
                print response['dealer']

host = 'localhost'
port = 10000
size = 1024
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


while True:
    command = raw_input("Insert command: ")
    if command == 'connect':
        name = raw_input("Insert name: ")
        print 'Connecting'
        try:
            s.connect((host, port))
            handler = Handler(s, size)
            playing = True
            handler.start()
        except socket.error as msg:
            print 'Cannot connect'
        s.send(json.dumps(Message(name).__dict__))

    elif command == 'send':
        data = raw_input("Insert data: ")
        s.send(json.dumps(Message(data).__dict__))

    elif command == 'recv':
        response = s.recv(size)
        print 'Response: \'' + response + '\''

    elif command == 'leave':
        playing = False
        s.send(json.dumps(Message(command).__dict__))
        break

    else:
        print 'Command \'' + command + '\' not known'

print 'Disconnect'
s.close()