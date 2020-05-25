import sys
import socket
import selectors
import types
import config as conf
import operator
from functools import reduce


class ServerGame:
    def __init__(self):
        self.field = [['.' for i in range(conf.field_size)] for j in range(conf.field_size)]
        self.field[2][2] = 'U'
        self.field[17][17] = 'U'
        pass

    def move(self, coord_from, coord_to):
        from_x, from_y = coord_from
        to_x, to_y = coord_to
        if self.field[from_x][from_y] != 'U':
            return False
        if self.field[to_x][to_y] != 'U':
            self.field[from_x][from_y] = '.'
            self.field[to_x][to_y] = 'U'
            return True
        pass

    def get_field(self):
        return ''.join(reduce(operator.concat, self.field))
    pass


class Server:
    def __init__(self, move_func, get_field):
        self.sel = selectors.DefaultSelector()
        self.move_func = move_func
        self.get_field = get_field
        self.user_number = 0
        self.users = {}
        self.game_status = 'waiting'
        pass

    def accept(self, sock, mask):
        conn, addr = sock.accept()
        self.users[addr] = conn
        print("accepted connection from", addr)
        conn.setblocking(False)
        self.sel.register(conn, selectors.EVENT_READ, self.read)

        self.user_number += 1
        pass

    def send_to_all(self, text):
        for conn in self.users.values():
            conn.sendall(text)

    def send_data(self, conn):
        if self.game_status == 'waiting':
            if self.user_number == 2:
                self.game_status = 'playing'
                text = 'start ' + self.get_field()
                self.send_to_all(text.encode('utf-8'))
            else:
                text = 'waiting'
                self.send_to_all(text.encode('utf-8'))
        elif self.game_status == 'playing':
            if self.user_number == 2:
                text = 'update ' + self.get_field()
                self.send_to_all(text.encode('utf-8'))
            else:
                text = 'exiting'
                self.send_to_all(text.encode('utf-8'))

        pass

    def parse_input(self, data):
        if data == 'hello':
            pass
        elif data[:4] == 'move':
            [from_x, from_y, to_x, to_y] = list(map(int, data[5:].split(' ')))
            self.move_func((from_x, from_y), (to_x, to_y))
        pass

    def read(self, conn, mask):
        recv_data = conn.recv(1024)  # Should be ready to read
        if recv_data:
            print('received ', recv_data.decode('utf-8'))

            self.parse_input(recv_data.decode('utf-8'))

            self.send_data(conn)
        else:
            print("closing connection to", conn)
            self.sel.unregister(conn)
            del self.users[conn.getpeername()]

            self.user_number -= 1
            conn.close()
        pass

    def run(self):
        if len(sys.argv) != 3:
            print("usage:", sys.argv[0], "<host> <port>")
            sys.exit(1)

        host, port = sys.argv[1], int(sys.argv[2])
        lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        lsock.setblocking(False)
        lsock.bind((host, port))
        lsock.listen()
        print("listening on", (host, port))
        self.sel.register(lsock, selectors.EVENT_READ, self.accept)

        while True:
            events = self.sel.select()
            for key, mask in events:
                callback = key.data
                callback(key.fileobj, mask)
        pass
    pass


def main():
    game = ServerGame()
    server = Server(game.move, game.get_field)
    server.run()
    pass


if __name__ == '__main__':
    main()
    pass
