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
                    self.handshake(player_socket[0])

                    message = json.loads(self.recv_data(player_socket[0]))

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

    def handshake(self, client):
        print 'Handshaking...'
        data = client.recv(Server.package_size)
        headers = self.parse_headers(data)

        digest = create_hash(headers['Sec-WebSocket-Key'])
        shake = "HTTP/1.1 101 Web Socket Protocol\r\n"
        shake += "Upgrade: WebSocket\r\n"
        shake += "Connection: Upgrade\r\n"
        shake += "Sec-WebSocket-Accept: " + digest + "\r\n\r\n"

        return client.send(shake)

    def parse_headers(self, data):
        headers = {}
        lines = data.splitlines()
        for l in lines:
            parts = l.split(": ", 1)
            if len(parts) == 2:
                headers[parts[0]] = parts[1]
        headers['code'] = lines[len(lines) - 1]
        return headers

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

        """
            method decodes receive data from HTML WebSocket client
        :return: nothing
        """
    def recv_data (self, client):
            # as a simple server, we expect to receive:
            #    - all data at one go and one frame
            #    - one frame at a time
            #    - text protocol
            #    - no ping pong messages
            data = bytearray(client.recv(Server.package_size))

            print data

            if(len(data) < 6):
                raise Exception("Error reading data")
            # FIN bit must be set to indicate end of frame

            assert(0x1 == (0xFF & data[0]) >> 7)
            # data must be a text frame
            # 0x8 (close connection) is handled with assertion failure
            assert(0x1 == (0xF & data[0]))

            # assert that data is masked
            assert(0x1 == (0xFF & data[1]) >> 7)
            datalen = (0x7F & data[1])

            str_data = ''
            if(datalen > 0):
                mask_key = data[2:6]
                masked_data = data[6:(6+datalen)]
                unmasked_data = [masked_data[i] ^ mask_key[i%4] for i in range(len(masked_data))]
                str_data = str(bytearray(unmasked_data))
            print str_data
            return str_data