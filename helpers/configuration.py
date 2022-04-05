import configparser
from pathlib import Path
from helpers.logs import logging


class Configuration:
    """
     Class to create a configuration file, update get values from same.  By default, when the create_config_file
     method is called it will create a configuration file with the name config.ini but can be change if desired.
     If it already exists no action is taken
    """

    def __init__(self, filename="config.ini"):
        
        self.filename = filename
        self.path = Path().parent.parent.resolve()

    def create_config_file(self):
        """
        create_config_file A method to create a configuration file in the root directory from with the scrip
        is running
        """

        self.name = Path(self.path).joinpath(str(self.filename))

        if not self.name.is_file():
            self.name.touch()
        else:
            return

    def add_config_sections(self, sections):
        """
        add_config_sections A method to add sections to the config.ini file.  If the config file doesn't exis
        it will attempt to create it by calling the create_config_file method

        Args:
            sections (list): A list of sections to be added to the config.ini file.  If the section
            already exists, it will be skipped
        """

        config = configparser.ConfigParser()
        config_file = Path(self.path).joinpath(str(self.filename))

        if not config_file.is_file():

            try:
                self.create_config_file()
            except Exception as e:
                return e
            else:
                with open(config_file, "a") as file:
                    config.read(config_file)

                    for section in sections:
                        if config.has_section(section):
                            continue
                        else:
                            config.add_section(section)

                    config.write(file)


