from logging import Logger


def logger(log_file: str = "finn.log", stream: bool = True) -> Logger:
    import logging

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    file_handler = logging.FileHandler(log_file)
    formatter = logging.Formatter(
        fmt="%(asctime)s | %(pathname)s | %(levelname)s | %(message)s",
        datefmt="%m-%d-%Y %H:%M:%S",
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    if stream:
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)
    return logger
