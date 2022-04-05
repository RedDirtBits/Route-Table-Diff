import configparser
from pathlib import Path
from helpers.logs import logging


class Configuration:
    """
     Class:

     Responsible for creating and managing a configuration file.  By default, when the create_config_file
     method is called it will create a configuration file with the name config.ini

        Methods:
     
            create_config_file - Creates the configuration file.  Does not need to be called directly as it
            will be called automatically with the add_config_section if the config.ini file is not found

            add_config_section - Takes a list as an argument and adds the item names in the list as sections
            to the configuration file if not already existing
    """

    def __init__(self, filename="config.ini"):
        
        self.filename = filename
        self.path = Path().parent.parent.resolve()

    def create_config_file(self):
        """
        create_config_file A method to create a configuration file in the root directory
        """

        self.name = Path(self.path).joinpath(str(self.filename))

        if not self.name.is_file():
            self.name.touch()
            logging.info(f"Created configuration file: {self.filename}")
        else:
            logging.info(f"The configuration file, {self.filename} no need to create it")

    def add_config_sections(self, sections):
        """
        add_config_sections A method to add sections to the config.ini file.  If the config file doesn't exist
        it will attempt to create it by calling the create_config_file method.  

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
                logging.error(f"Creation of the configuration file errored with error message: {e}")
            else:
                with open(config_file, "a") as file:
                    config.read(config_file)

                    for section in sections:
                        if config.has_section(section):
                            continue
                        else:
                            config.add_section(section)
                            logging.info(f"Added {section} section to the configuration file")

                    config.write(file)
                    logging.info(f"Configuration file has been updated with the provided sections")

    def get_config_value(self, section, param):
        pass


