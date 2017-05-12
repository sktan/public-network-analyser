""" Performs reconnaissance on current networks  """
import sys
import platform
from libs.netrecon import NetRecon
# pip install pyspeedtest
import pyspeedtest

def print_os():
    """ Prints the OS to the console """
    print("Current Operating System: {} {}".format(platform.system(), platform.release()))

def network_interface():
    """ Grabs the network interface information """
    net_out_ip = NetRecon.out_interface()
    print("LAN Address: {0}".format(net_out_ip))
    print("External IP: {0}".format(NetRecon.get_external_ip()))
    return None

def speedtest():
    """ Runs a internet speedtest """
    net_speed = pyspeedtest.SpeedTest()
    print("Ping: {0}".format(int(net_speed.ping())))
    print("Download Speed: {0}".format(format_network_speed(net_speed.download())))
    print("Upload Speed: {0}".format(format_network_speed(net_speed.upload())))

def format_network_speed(raw_bps=0):
    """ Formats a network speed test to human readable format """
    fmt = ['b/s', 'Kb/s', 'Mb/s', 'Gb/s']
    index = 0
    speed = raw_bps
    while speed > 1024:
        index += 1
        speed /= 1024
    return "%0.2f %s" % (speed, fmt[index])

def main(args=None):
    """ The entry point of our script."""
    if args is None:
        args = sys.argv[1:]

    print_os()
    network_interface()
    speedtest()

if __name__ == "__main__":
    main()
