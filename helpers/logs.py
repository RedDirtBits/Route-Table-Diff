import logging

"""
    Configure the logger
"""

# Configure the logging
logging.basicConfig(
    filename="application.log",
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] (%(module)s):\n Message: %(message)s',
    filemode='a',
    )