##################################################################################################
#                                     LOGGING CONFIGURATION                                      #
#                                                                                                #
# Sets up a consistent colored logger to be reused throughout the project.                       #
##################################################################################################

##################################################################################################
#                                            IMPORTS                                             #
##################################################################################################

import logging
import sys
import colorlog

##################################################################################################
#                                      LOGGER INITIALIZATION                                     #
##################################################################################################

logger = logging.getLogger("NERLogger")
logger.setLevel(logging.INFO)

if not logger.hasHandlers():
    handler = colorlog.StreamHandler(sys.stdout)
    formatter = colorlog.ColoredFormatter(
        "%(log_color)s[%(asctime)s] [%(levelname)s] %(message)s",
        datefmt="%H:%M:%S",
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'bold_red',
        }
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
