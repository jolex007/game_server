import socket
import sys
import config as conf


class WebModule:
    def __init__(self, ready_to_play, update_field):
        if len(sys.argv) != 3:
            print('usage:', sys.argv[0], '<host> <port>')
            return

        self.ready_to_play = ready_to_play
        self.update_field = update_field
        self.host, self.port = sys.argv[1], int(sys.argv[2])
        self.sock = socket.socket()

        pass

    def start_game(self):
        self.ready_to_play()
        pass

    def convert_field_data(self, data):
        field = [['.' for i in range(conf.field_size)] for j in range(conf.field_size)]
        for x in range(conf.field_size):
            for y in range(conf.field_size):
                field[x][y] = data[x * conf.field_size + y]
        return field
        pass

    def parse_data(self, data):
        if data[:7] == 'waiting':
            return
        elif data[:5] == 'start':
            print(data[6:])
            self.update_field(self.convert_field_data(data[6:]))
            self.start_game()
        elif data[:6] == 'update':
            self.update_field(self.convert_field_data(data[7:]))
        pass

    def send_command(self, command):
        self.sock.send(command.encode('utf-8'))
        pass

    def start(self):
        try:
            self.sock.connect((self.host, self.port))
            print('connected')
            self.sock.send('hello'.encode('utf-8'))
            while True:
                data = self.sock.recv(1024)
                if data:
                    self.parse_data(data.decode('utf-8'))
        except KeyboardInterrupt:
            print('Keyboard Interrupt')
        finally:
            self.sock.close()

        pass

    pass
