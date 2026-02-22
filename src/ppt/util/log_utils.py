"""Contains functions that relate to logging."""

import json
import logging.config
import pathlib

logger = logging.getLogger(__name__)

DEFAULT_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "log_file": {
            "format": "%(asctime)s - %(levelname)s - %(name)s - %(lineno)d - \n\t%(message)s\n",  # noqa: E501
            "datefmt": "%Y-%m-%dT%H:%M:%SZ",
        },
        "log_stream": {
            "format": "%(levelname)s - %(name)s - %(lineno)d - %(message)s"
        },
    },
    "handlers": {
        "debug_file_handler": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": logging.INFO,
            "formatter": "log_file",
            "filename": "./logs/app.log",
            "maxBytes": 100_485_760,
            "backupCount": 3,
            "encoding": "utf8",
            "mode": "a",
        },
        "consoleHandler": {
            "class": "logging.StreamHandler",
            "formatter": "log_stream",
            "level": logging.DEBUG,
        },
    },
    "root": {
        "level": logging.DEBUG,
        "handlers": [
            "debug_file_handler",
            "consoleHandler",
        ],
    },
}


def generate_log_location(log_path: pathlib.Path | str | None = None) -> str:
    """Create folder structure for logs, if any folders are missing.

    Take in a potential log filepath, and then verify the parent folders exist.

    :param log_path: The path to the log file in question,
                     defaults to log folder in the project root.
    :type log_path: pathlib.Path | str | None, optional
    :return: The path where log files will be stored.
    :rtype: str
    """

    # Default is log folder in root of project.
    default_path = pathlib.Path(__file__).parents[3] / "logs"

    if log_path is None:
        log_path = default_path
    else:
        try:
            log_path = pathlib.Path(log_path).resolve().parent
        except TypeError:
            log_path = default_path

    if not log_path.exists():
        log_path.mkdir(exist_ok=True)

    return str(log_path)


def setup_logging(
    cfg_path: str | pathlib.Path | None = None, log_level: int = 0
) -> None:
    """Configure logging based on log cfg file if possible,
       Otherwise, then use default configuration.

    :param cfg_loc: Location of config file, defaults to ./.configs/log.conf
    :type cfg_loc: str | pathlib.Path | None, optional
    :param log_level: Denotes what type of messages will be logged,
                      defaults to all messages.
    :type log_level: int, optional
    """

    if cfg_path is None:
        cfg_path = "./.configs/log.conf"

    try:
        with open(cfg_path) as file:
            log_dict = json.load(file)
        log_method = "Configuration loaded from %s"
    except FileNotFoundError:
        log_method = "%s not found, using default configuration."
        log_dict = DEFAULT_CONFIG

    # Logging module does not create folder structure for missing parents
    log_file_info = []
    for handler in log_dict["handlers"]:
        log_file = log_dict["handlers"][handler].get("filename", False)
        if log_file:
            log_path = generate_log_location(log_file)
            log_file_info.append((handler, log_path))

    logging.config.dictConfig(log_dict)
    logger.setLevel(log_level)
    logger.info(log_method, pathlib.Path(cfg_path).resolve())

    for handler, location in log_file_info:
        logger.info("Handler: %s, Location: %s", handler, location)


setup_logging()
