import ipaddress
from helpers.logs import logging

def ip4_validate(ipaddr):
    """
    ip4_validate Validates an IPv4 address using the ipaddress library

    Args:
        ipaddr (str): The IP address to be validated

    Returns:
        bool: True if it is a valid IPv4 addres, False otherwise
    """

    try:
        ipaddress.ip_address(ipaddr)
        logging.info(f"{ipaddr} is a valid IPv4 address")
        return True
    except (ipaddress.AddressValueError,ValueError):
        logging.error(f"{ipaddr} is not a valid IPv4 address")
        return False