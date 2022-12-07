import logging


def create_logger():
    """Creates a logger with settings"""
    logger = logging.getLogger("Logger for Scraper")
    logger.setLevel(logging.DEBUG)

    # Create Formatter
    formatter = logging.Formatter(
        '%(asctime)s-%(levelname)s-FILE:%(filename)s-FUNC:%(funcName)s-LINE:%(lineno)d-%(message)s')

    # create a file handler and add it to logger
    file_handler = logging.FileHandler("logs.log")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger


logger = create_logger()
