import select
import socket
import sys
import accept_player
from core.table import Table


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
                    print 'Connection from ' + str(player_socket[1])
                    accept_player.AcceptPlayer(self, player_socket).start()

                elif s == sys.stdin:
                    command = sys.stdin.readline().rstrip('\n')
                    if command == 'exit':
                        print 'Closing server'
                        self.delete_empty_tables()
                        running = False
                    else:
                        print 'Command \'' + command + '\' not known'

        self.server.shutdown(socket.SHUT_RDWR)
        self.server.close()
        for table in self.tables:
            table.killed = True
            table.join()
        print 'Server closed'

    def open_socket(self):
        """
            tries to open server socket
        :return: nothing
        """
        try:
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
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
            if table.is_empty():
                table.killed = True
                table.join()
                self.tables.remove(table)
                i -= 1
                print 'Empty table removed'
