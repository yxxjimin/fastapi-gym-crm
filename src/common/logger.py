import logging
import sys


def getLogger(name: str, logging_level: int = logging.DEBUG) -> logging.Logger:
    logger = logging.getLogger(name)
    logging.basicConfig(
        stream=sys.stdout,
        encoding="utf-8",
        level=logging_level,
        format="%(asctime)s [%(levelname)-8s] %(filename)s:%(lineno)d -- %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    return logger
