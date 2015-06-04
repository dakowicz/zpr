import select
import socket
import sys
import json
import game.player
from core.table import Table
import base64
import hashlib


def create_hash(key):
    hash = hashlib.sha1(key + "258EAFA5-E914-47DA-95CA-C5AB0DC85B11")
    return base64.b64encode(str(hash.digest()))


def recv_data(client, length):
    data = client.recv(length)
    if not data: return data
    return data.decode('utf-8', 'ignore')


def send_data(client, data):
    message = "\x00%s\xFF" % data.encode('utf-8')
    return client.send(message)


def parse_headers(data):
    headers = {}
    lines = data.splitlines()
    for l in lines:
        parts = l.split(": ", 1)
        if len(parts) == 2:
            headers[parts[0]] = parts[1]
    headers['code'] = lines[len(lines) - 1]
    return headers


def handshake(client):
    print 'Handshaking...'
    data = client.recv(1024)
    headers = parse_headers(data)
    print 'Got headers:'
    for k, v in headers.iteritems():
        print k, ':', v

    digest = create_hash(headers['Sec-WebSocket-Key'])
    shake = "HTTP/1.1 101 Web Socket Protocol\r\n"
    shake += "Upgrade: WebSocket\r\n"
    shake += "Connection: Upgrade\r\n"
    shake += "Sec-WebSocket-Accept: " + digest + "\r\n\r\n"

    return client.send(shake)


class Server:
    package_size = 1024

    def __init__(self):
        self.host = ''
        self.port = 10000
        self.backlog = 5
        self.server = None
        self.tables = []
        print 'Server created'

    def run(self):
        """
            server main function - listen for players and place them by tables
            to close server type 'exit' in standard input
        :return: nothing
        """
        self.open_socket()
        input = [self.server, sys.stdin]
        running = True
        print 'Server running'
        while running:
            input_ready, output_ready, except_ready = select.select(input, [], [])

            for s in input_ready:
                if s == self.server:
                    player_socket = self.server.accept()
                    handshake(player_socket[0])

                    message = json.loads(player_socket[0].recv(Server.package_size))
                    name = message['content']
                    print 'New player: ' + name
                    self.get_table().add_player(game.player.Player(name, player_socket))

                elif s == sys.stdin:
                    command = sys.stdin.readline().rstrip('\n')
                    if command == 'exit':
                        print 'Closing server'
                        self.delete_empty_tables()
                        running = False
                    else:
                        print 'Command \'' + command + '\' not known'

        self.server.close()
        for table in self.tables:
            table.join()
        print 'Server closed'

    def open_socket(self):
        """
            tries to open server socket
        :return: nothing
        """
        try:
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server.bind((self.host, self.port))
            self.server.listen(self.backlog)
        except socket.error, (value, message):
            if self.server:
                self.server.close()
            print "Could not open socket: " + message
            sys.exit(1)

    def get_table(self):
        """
            firstly, method deletes empty tables on which game has ended
            returns table by which player can sit or if such doesn't exist, returns new one
        :return: Table
        """
        self.delete_empty_tables()

        for table in self.tables:
            if not table.started and not table.is_full():
                return table

        new_table = Table()
        self.tables.append(new_table)
        print 'New table created'
        new_table.start()
        return new_table

    def delete_empty_tables(self):
        """
            method deletes tables on which game has ended and all players have left
        :return: nothing
        """
        i = 0
        while i < len(self.tables):
            table = self.tables[i]
            i += 1
            if table.is_empty() and table.started:
                table.join()
                self.tables.remove(table)
                i -= 1
                print 'Empty table removed'
