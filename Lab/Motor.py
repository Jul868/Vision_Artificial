import socket

class MotorController:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = None

    def connect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))

    def rotate_servo(self, degrees):
        if self.sock:
            message = str(degrees).encode('utf-8')
            self.sock.sendall(message)

    def close(self):
        if self.sock:
            self.sock.close()
            self.sock = None
