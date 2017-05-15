""" Performs reconnaissance on current networks  """
import sys
import platform
from libs.netrecon import NetRecon
# pip install pyspeedtest
import pyspeedtest

def operating_system():
    """ Prints the OS to the console """
    os_string = "{} {}".format(platform.system(), platform.release())
    print("Current Operating System: %s" % os_string)
    return os_string

def network_interface():
    """ Grabs the network interface information """
    net_out_ip = NetRecon.out_interface()
    ext_ip = NetRecon.get_external_ip()
    print("LAN Address: {0}".format(net_out_ip))
    print("External IP: {0}".format(ext_ip))
    # Returns a dictionary with the internal + external IPs
    return {
        'external_ip': ext_ip,
        'internal_ip': net_out_ip
    }

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

def requires_captive_portal():
    """ Determines whether a captive portal is required for this network """
    cap_por_required = NetRecon.captive_portal_required()
    print("Captive portal: {0}".format(cap_por_required))

def main(args=None):
    """ The entry point of our script."""
    if args is None:
        args = sys.argv[1:]

    network_stats = {}
    operating_system()
    network_interface()
    requires_captive_portal()
    speedtest()

if __name__ == "__main__":
    main()
