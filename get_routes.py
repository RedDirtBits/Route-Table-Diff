import time
import pathlib
import csv

from netmiko import ConnectHandler, NetmikoTimeoutException, NetmikoAuthenticationException
from ntc_templates.parse import parse_output
from datetime import datetime

from helpers.constants import Constant
from helpers.validation import ip4_validate
from helpers.ping import ip4_ping
from helpers.open_file import open_device_list_file
from helpers.logs import logging
from helpers.commands import RunCommand
from credentials.credentials import GetCredentials

# Set a starting timer.  Mainly for initial testing
START_TIME = time.time()
TIMESTAMP = datetime.now().strftime("%m-%d-%Y_T%H:%M:%S")

# The first log entry when the application starts will deliniate when it
# has started and the root directory in which the script is running

logging.info("#" * 25 + " Application Starting " + "#" * 25)
logging.info(f"Working Directory: {Constant.script_path()}\n")

# Loop through the file containg the devices to be connected to and create the connection
# profile
for device in open_device_list_file(Constant.devices_list() / "devices.txt"):

    # As a sanity check validate that the IP address is, in fact, a valid IP address then
    # ping it to see if it can be reached.  If either fails, abort the process
    if ip4_validate(device[0]) and ip4_ping(device[0]):

        device_ssh_connection = {
            "host": device[0],
            "device_type": device[1],
            "username": GetCredentials.netlab_user(),
            "password": GetCredentials.netlab_passwd(),
            "secret": GetCredentials.netlab_enable()
        }

        logging.info(f"Created SSH Connection profile for {device[0]}")

        try:

            # Only running a single command
            command = RunCommand.show_routes()

            # Connect to the device
            with ConnectHandler(**device_ssh_connection) as ssh_connection:
                
                # Activate enable mode
                ssh_connection.enable()
                # Grab the hostname.  Assumes the name at the command prompt is the hostname
                hostname = ssh_connection.find_prompt()[:-1]
                # Store the raw output of the command run in a variable
                raw_output = ssh_connection.send_command(command)

                logging.info(f"Console Output for {device[0]} running command: {command}\n\n{raw_output}")

                # Parse the command output into a format that is easier to work with.  Making the platform and
                # command dynamic, we automatically get the correct template output which is helpful later when 
                # the output is written to a CSV file.
                parsed_output = parse_output(platform=device[1], command=command, data=raw_output)

                ###################################################################################
                # Above here, the code is pretty universal across different use cases since we are
                # merely setting up the connection and then connecting to the devices.  Below this
                # is where the processing of the output begins.
                ###################################################################################

                # Save the routes in a separate directory with subdirectories named after the hostname
                # If it were just one or two devices it would probably not matter, but since there
                # may potentially be several, lets structure things so they are easy to find
                #
                # Create that structure here
                tables_dir = pathlib.Path.cwd() / f"routes/{hostname}"
                tables_dir.mkdir(parents=True, exist_ok=True)

                # Because, ultimately, we want to compare the routes as they are now with post-migration routes
                # We need to separately identify the first run from all others.  Here we check if the first run
                # file exists (ending in _original_routes.csv), then we check if there are any subsequent files
                # (ending in _migrated_xxx.csv).  If they do exist, loop through until we can create a unique
                # filename with the next number increment.
                if pathlib.Path(tables_dir / f"{hostname}_original_routes.csv").is_file():
                    i = 1
                    while pathlib.Path(tables_dir / f"{hostname}_migrated_{i:03d}.csv").is_file():
                        i += 1
                    csv_filename = f"{hostname}_migrated_{i:03d}.csv"
                else:
                    csv_filename = f"{hostname}_original_routes.csv"

                try:
                    with open(pathlib.Path(tables_dir / csv_filename), "w") as csv_file:

                        for route in parsed_output:

                            # since the dictionary keys are different for typical Cisco routers and Nexus devices, we grab the device type
                            # (device[1]) from the host lists file and use the appropriate key/value pairs depending on the device
                            if device[1] == "cisco_nxos":

                                field_names = ["vrf", "protocol", "type", "network", "mask", "distance", "metric", "nexthop_ip", "nexthop_if"]
                                writer = csv.DictWriter(csv_file, fieldnames=field_names)
                                writer.writeheader()

                                writer.writerow({
                                    "vrf": route["vrf"],
                                    "protocol": route["protocol"],
                                    "type": route["type"],
                                    "network": route["network"],
                                    "mask": route["mask"],
                                    "distance": route["distance"],
                                    "metric": route["metric"],
                                    "nexthop_ip": route["nexthop_ip"],
                                    "nexthop_if": route["nexthop_if"]
                                })

                            elif device[1] == "cisco_ios":

                                field_names = ["protocol", "type", "network", "mask", "distance", "metric", "nexthop_ip", "nexthop_if"]
                                writer = csv.DictWriter(csv_file, fieldnames=field_names)
                                writer.writeheader()

                                writer.writerow({
                                    "protocol": route["protocol"],
                                    "type": route["type"],
                                    "network": route["network"],
                                    "mask": route["mask"],
                                    "distance": route["distance"],
                                    "metric": route["metric"],
                                    "nexthop_ip": route["nexthop_ip"],
                                    "nexthop_if": route["nexthop_if"]
                                })


                        logging.info(f"Created {csv_filename} in {tables_dir}")

                except ValueError:

                    # If the field names don't match names in the writerow action, it will throw a ValueError
                    logging.error(
                        f"There was an error when trying to write to the CSV file.\n \
                        If it contains only the header row, check the writerow field names"
                        )

        except NetmikoAuthenticationException:
            logging.error(f"Authentication failed. Invalid username or password for {device[0]}. Please verify your credentials")
        except NetmikoTimeoutException:
            logging.error(f"Connection time out for {device[0]}")
        except ValueError:
            logging.error(f"Failed to enter privilege mode! Please check the enable password for device {device[0]}")

    else:
        logging.error(f"Failed to create a connection profile for {device[0]}")
        continue

END_TIME = time.time()

logging.info("#" * 25 + " Application Finished " + "#" * 25)
logging.info(f"Script Execution took {END_TIME - START_TIME} seconds")