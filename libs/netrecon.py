""" Class for network functions """
import socket

class NetRecon:
    """ Class for network functions """
    @staticmethod
    def out_interface():
        """ Gets the network IP address that has a route out """
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.connect(("8.8.8.8", 80))
        return sock.getsockname()[0]
    @staticmethod
    def ping_subnet():
        """ Pings an entire subnet of IP addresses """
        
