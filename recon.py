""" Performs reconnaissance on current networks  """
import sys
import platform
import configparser
import json
from libs.netrecon import NetRecon
# pip install pyspeedtest
import pyspeedtest

# Allows us to utilise a global config file
# recon.ini
config = configparser.ConfigParser() # pylint: disable=invalid-name
config.read('recon.ini')

def operating_system():
    """ Prints the OS to the console """
    os_string = "{} {}".format(platform.system(), platform.release())
    print("Current Operating System: %s" % os_string)
    return os_string

def network_interfaces():
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
    ping = net_speed.ping()
    download = net_speed.download()
    upload = net_speed.upload()
    print("Ping: {0}".format(int(ping)))
    print("Download Speed: {0}".format(format_network_speed(download)))
    print("Upload Speed: {0}".format(format_network_speed(upload)))
    return {
        'ping': ping,
        'download': download,
        'upload': upload
    }

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
    return cap_por_required

def check_openvpn():
    """ Sends a test UDP packet to an OpenVPN server """
    ovpn_result = NetRecon.check_openvpn(
        config['openvpn']['host'],
        port=int(config['openvpn']['port'])
        )
    print("OpenVPN connectivitiy: {0}".format(ovpn_result))
    return ovpn_result

def main(args=None):
    """ The entry point of our script."""
    if args is None:
        args = sys.argv[1:]

    network_stats = {}
    network_stats['os'] = operating_system()
    network_stats['network_interfaces'] = network_interfaces()
    cap_required = requires_captive_portal()
    network_stats['captive_portal_required'] = cap_required
    if not cap_required:
        network_stats['internet_speeds'] = speedtest()
        network_stats['openvpn_allowed'] = check_openvpn()
    else:
        print("Captive portal required, please login before proceeding.")
        print("Network stats incomplete due to captive portal requirement.")
    print("JSON Output:")
    # prints some pretty json output :D
    # We should be able to submit this output to a website for
    # pretty display of the collected data
    print(json.dumps(network_stats, indent=4, sort_keys=True))

if __name__ == "__main__":
    main()
