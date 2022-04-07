import logging

"""
    Configure the logger
"""

# Configure the logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] (%(module)s):\n Message: %(message)s',
    handlers=[
        logging.FileHandler("application.log", "a"),
        logging.StreamHandler()
    ])