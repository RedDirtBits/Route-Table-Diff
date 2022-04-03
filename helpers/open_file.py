from helpers.logs import logging

def open_device_list_file(filename):
    """
    open_device_list_file Opens the file containing the information (ip/hostname and device type)
    for the device(s) to be connected to

    Args:
        filename (str): The filename to be opened

    Returns:
        list: Contains the IP/hostname of the device to be connected to and its device type
        for use with Netmiko

        Device type can be "cisco_ios" for typical routers and switches, "cisco_nxos" for Nexus devices
        or even "cisco_ios_telnet" for devices still using Telnet **gasp**
    """

    device_list = []

    try:
        with open(filename, 'r') as file:

            for line in file.readlines():
                host, device_type = line.strip().split(',')
                device_list.append((host, device_type))

    except (IOError, FileNotFoundError):
        logging.error(f"Unable to open the filename provided: {filename}")
        return f"Unable to open the provided file: {filename}."
    else:
        logging.info(f"\t Processed {filename}\n Devices found:\t {device_list}")
        return device_list
