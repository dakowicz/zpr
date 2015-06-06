import threading
import select
import json
import websocket
import game.player
import server


class AcceptPlayer(threading.Thread):
    TIMEOUT = 150

    def __init__(self, game, (socket, address)):
        threading.Thread.__init__(self)
        self.game = game
        self.socket = socket
        self.address = address

    def run(self):
        """
            waits until new player a insert his name, timeout set on 20 seconds
            adds accepted player to proper table
        :return: nothing
        """
        try:
            websocket.handshake(self.socket)
            input_ready, output_ready, except_ready = select.select([self.socket], [], [], self.TIMEOUT)
            if len(input_ready) == 0:
                print 'Player is not accepted - waited too long'
                return
            message = json.loads(websocket.recv_data(self.socket, server.Server.package_size))
            name = message['content']
            print 'New player: ' + name
            self.game.get_table().add_player(game.player.Player(name, self.socket))
        except Exception as msg:
            print msg

