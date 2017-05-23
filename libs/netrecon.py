""" Class for network functions """
# pylint: disable=W0702
import socket
# pip install dnspython
import dns.resolver
from libs.webtools import WebTools

class NetRecon:
    """ Class for network functions """
    @staticmethod
    def out_interface():
        """ Gets the network IP address that has a route out """
        # http://stackoverflow.com/a/166589
        # Connects to an internet resource (google's DNS)
        # and then returns the IP address that was used to connect
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.connect(("8.8.8.8", 80))
        out_ip = sock.getsockname()[0]
        sock.close()
        return out_ip
    @staticmethod
    def ping_subnet():
        """ Pings an entire subnet of IP addresses """
    @staticmethod
    def get_external_ip():
        """ Grabs the external IP address """
        address = ""
        try:
            # We will first use the OpenDNS DNS server to grab our public IP
            # Basically the equivilent to dig +short myip.opendns.com @resolver1.opendns.com
            my_resolver = dns.resolver.Resolver()
            my_resolver.timeout = 1
            my_resolver.lifetime = 1
            my_resolver.nameservers = ['208.67.222.222']
            answer = my_resolver.query('myip.opendns.com.')
            address = answer[0].address
        except:
            # HTTP fallback on Akamai's CDN
            # http://whatismyip.akamai.com/
            request = WebTools.get("http://whatismyip.akamai.com/")
            address = request['response']
        return str(address)
    @staticmethod
    def captive_portal_required():
        """ Determine if a captive portal login is required for this network """
        # We will use the google endpoint below to look for a "NO CONTENT" HTTP status
        url = "http://clients3.google.com/generate_204"
        # If a 3xx or 200 response, we can determine that a captive portal is required
        # https://www.chromium.org/chromium-os/chromiumos-design-docs/network-portal-detection
        request = WebTools.get(url, expected_response=204)
        return request['status'] != 204
    @staticmethod
    def check_openvpn(ip_addr, port=1194):
        """ Determine if port 1194 UDP is allowed for OpenVPN connections """
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(10)
        sock.connect((ip_addr, port))
        # Send TLS initialisation command
        # https://serverfault.com/a/470065
        # equivilent to echo -e "\x38\x01\x00\x00\x00\x00\x00\x00\x00" |
        # timeout 10 nc -u openvpnserver.com 1194 | cat -v
        sock.send(bytes([0x38, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]))
        retval = True
        try:
            data = str(sock.recv(100))
        except:
            retval = False
        sock.close()
        return retval
