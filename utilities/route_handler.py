import pathlib
import json


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



    def compare_routes(self):
        pass
