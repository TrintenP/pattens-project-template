import json
import logging.config

logger = logging.getLogger(__name__)


def test():
    with open(".configs/log.conf") as file:
        log_dict = json.load(file)

    logging.config.dictConfig(log_dict)
    logger.setLevel(logging.DEBUG)
    logger.info("Test")


test()
