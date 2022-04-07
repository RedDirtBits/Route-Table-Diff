import pathlib
import json
from termios import FF1

from helpers.logs import logging


class ProcessRoutes():

    def save_routes(self, host: str, routes: list):
        """
        save_routes: A function that takes a routing table parsed through NTC 
        templates and saves it to a JSON file.  The filename will contain
        _original.json if it is the first file created for the device to denote
        this is the state of the routing table before any work is done.  If
        the _original file exists, then all subsequent file saves will contain
        _migrated.json to denote changes from the original.  This file can also
        be overwritten so that the original state can be compared to the 
        current state.

        Args:
            host (str): Hostname of the device for which the routing table belongs

            routes (list): The list of dictionaries returned from NTC templates
            parse_output
        """

        try:
            # Try to get the stats of the file.  If it doesn't exist, it will raise an
            # exception
            pathlib.Path(f"{host}_original.json").stat()

        except FileNotFoundError:

            # As a sanity check, because we need to REALLY avoid overwriting the _original
            # file, lets check if the file exists one more time.  If it doesn't, we can
            # proceed
            if not pathlib.Path(f"{host}_original.json").is_file():
                with open(pathlib.Path(f"{host}_original.json"), "w") as f:
                    f.write(json.dumps(routes))
        else:

            # If there is no exception raised we know the _original file exists so every
            # run of the script now will create a _migrated version which CAN be overwritten
            with open(pathlib.Path(f"{host}_migrated.json"), "w") as f:
                f.write(json.dumps(routes))


        # if not pathlib.Path(f"{host}_original.json").is_file():

        #     with open(pathlib.Path(f"{host}_original.json"), "w") as f:
        #         f.write(json.dumps(routes))
        # else:

        #     with open(pathlib.Path(f"{host}_migrated.json"), "w") as f:
        #         f.write(json.dumps(routes))


    def compare_routes(self, host: str, original_file: str, migrated_file: str):
        """
        compare_routes Compares the pre-migration and post-migration routing tables of a device for the purpose
        of identifying routes that did not come back afte the migration has completed.

        Args:
            host (str): The hostname of the device from which the routes were pulled

            original_file (str): The file that contains the routing table pre-migration.  A list of dictionaries from
            the NTC template parsing in .json format

            migrated_file (str): The file that contains the routing table post-migration.  A list of dictionaries from
            the NTC template parsing in .json format

        Raises:
            FileExistsError: Error raised if either of the files required are not found
        """
        
        try:
            # Clearly the files should exit, but you know what assume does to you
            # For the sake of sanity, let's make sure.  If not, raise an error
            if not pathlib.Path(original_file).exists() and not pathlib.Path(migrated_file).exists():
                raise FileExistsError
            else:
                # The files are present, open and load them for comparison
                with open(original_file, "r") as f1, open(migrated_file, "r") as f2:
                    original = json.load(f1)
                    migrated = json.load(f2)

                    # The original file is the master file.  Loop through that file and look for routes
                    # that are in it that are not in the migrated routes file
                    for i in original:
                        if i not in migrated:
                            # For now, just print out the differences.  Needs work
                            print(i)
                        
        except FileExistsError:
            logging.error(f"{original_file} or {migrated_file} could not be found")
