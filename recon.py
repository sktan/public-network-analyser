""" Performs reconnaissance on current networks  """
import sys
import platform
from libs.netrecon import NetRecon
import pyspeedtest

def print_os():
    """ Prints the OS to the console """
    print("Current Operating System: {} {}".format(platform.system(), platform.release()))

def network_interfaces():
    """ Grabs the network interface information """
    net_out_ip = NetRecon.out_interface()
    print(net_out_ip)
    return None

def speedtest():
    """ Runs a internet speedtest """
    net_speed = pyspeedtest.SpeedTest()
    print(int(net_speed.ping()))
    print(format_network_speed(net_speed.download()))
    print(format_network_speed(net_speed.upload()))

def format_network_speed(raw_bps=0):
    """ Formats a network speed test to human readable format """
    fmt = ['b/s', 'Kb/s', 'Mb/s', 'Gb/s']
    index = 0
    speed = raw_bps
    while speed > 1024:
        index += 1
        speed /= 1024
    return "%0.2f %s" % (int(speed), fmt[index])

def main(args=None):
    """ The entry point of our script."""
    if args is None:
        args = sys.argv[1:]

    print_os()
    network_interfaces()
    speedtest()

if __name__ == "__main__":
    main()
