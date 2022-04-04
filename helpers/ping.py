import icmplib

from logs import logging

def ip4_ping(ip4_addr, packets = 2):
    """
    ip4_ping A simple pinger that will send icmp packets to the ip address provided using
    the icmplib library

    Args:
        ip4_addr (str): The IP address of the device to be pinged

    Returns:
        bool: True if the device is pingable, False otherwise.
    """   

    ping_ip = icmplib.ping(ip4_addr, interval=0.5, count=packets, privileged=False)

    if ping_ip.packets_received == 0:
        logging.info(f"{ip4_addr} is not responding to ping.  Request retuned {ping_ip.packets_received} of {packets} packets sent")
        return False
    else:
        logging.info(f"{ip4_addr} responded to ping and is reachable. Avg. Response Time: {ping_ip.avg_rtt}")
        return True
