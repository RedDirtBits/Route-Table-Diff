import icmplib

from helpers.logs import logging

def ip4_ping(ip4_addr):
    """
    ip4_ping A simple pinger that will send icmp packets to the ip address provided using
    the icmplib library

    Args:
        ip4_addr (str): The IP address of the device to be pinged

    Returns:
        bool: True if the device is pingable, False otherwise.
    """   

    packet_count = 2
    ping_ip = icmplib.ping(ip4_addr, interval=0.5, count=packet_count, privileged=False)

    if ping_ip.packets_received == 0:
        logging.info(f"{ip4_addr} is not responding to ping.  Request retuned {ping_ip.packets_received} of {packet_count} packets sent")
        return False
    else:
        logging.info(f"{ip4_addr} responded to ping and is reachable. Avg. Response Time: {ping_ip.avg_rtt}")
        return True
