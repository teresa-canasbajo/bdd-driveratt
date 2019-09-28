import socket
import logging, time

class UDPsocket:  
    """
    Simple python object to bind to a UDP socket. 
    """

    def __init__(self, ip, port, buffersize=1024):
        self.ip = ip
        self.port = port
        self.buffersize = buffersize
        self.logger = logging.getLogger(__name__)
        self.logger.info('Creating UDP socket object')

    def sock_bind(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.ip, self.port))
        self.logger.info("Socket bound to {}:{}.".format(self.ip, self.port))

    def sock_listen(self):
        """
        listen to the socket via recvfrom(), 
        which only runs once, thus requiring iteration.
        """
        self.data, self.addr = self.sock.recvfrom(1024)
        self.t1s = int(round(time.time()*1000))
        self.logger.info("Received buffer: {}.".format(self.data))
        return (self.data, self.t1s)
