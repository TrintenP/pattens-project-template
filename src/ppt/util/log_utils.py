"""Contains functions that relate to logging."""

import functools
import json
import logging
import logging.config
import pathlib
import time
import typing

logger = logging.getLogger(__name__)

DEFAULT_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "log_stream": {
            "format": "%(asctime)s - %(levelname)s - %(name)s - %(lineno)d - \n\t%(message)s\n",  # noqa: E501
        },
    },
    "handlers": {
        "consoleHandler": {
            "class": "logging.StreamHandler",
            "formatter": "log_stream",
            "level": logging.DEBUG,
        },
    },
    "root": {
        "level": logging.DEBUG,
        "handlers": [
            "consoleHandler",
        ],
    },
}


def generate_log_location(log_path: pathlib.Path | str = "") -> str:
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

    if not log_path:
        log_path = default_path
    else:
        try:
            log_path = pathlib.Path(log_path).resolve().parent
        except TypeError:
            log_path = default_path

    if not log_path.exists():
        log_path.mkdir(exist_ok=True)

    return log_path.as_posix()


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
            cfg = json.load(file)
        log_method = "Configuration loaded from %s"
    except FileNotFoundError:
        log_method = "%s not found, using default configuration."
        cfg = DEFAULT_CONFIG

    handlers:list[str] = [h.get("filename", "") for h in cfg.get("handlers",{}).values()]  # ty:ignore[possibly-missing-attribute, invalid-assignment]  # noqa: E501 #fmt:skip

    for log_file in handlers:
        if log_file:
            #  Logging module doesn't create missing parents
            log_path = generate_log_location(log_file)
            logger.info("New log file at %s", log_path)

            logging.config.dictConfig(cfg)
            logging.Formatter.converter = time.gmtime  # Needed for ISO 8601
            logger.setLevel(log_level)
            logger.info(
                log_method, pathlib.Path(cfg_path).resolve().as_posix()
            )


# More info found at: https://ankitbko.github.io/blog/2021/04/logging-in-python/
def enable_logging(_func: typing.Callable) -> typing.Callable:
    """Creates a standard logging format for functions.

    Will denote the signature for a function, and if it returns any errors.

    :param _func: Function to be logged.
    :type _func: typing.Callable
    :return: Function with standardized logging.
    :rtype: typing.Callable
    """

    def decorate_func(func):
        # Allows the function being wrapped to maintain signature
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            args_repr = [repr(a) for a in args]
            kwargs_repr = [f"{kwargs=}"]
            func_name = func.__name__
            signature = ", ".join(args_repr + kwargs_repr)
            logger.debug(
                "Function %s called with args %s", func_name, signature
            )

            try:
                returned_val = func(*args, **kwargs)
                return returned_val
            except Exception as e:
                logger.exception(
                    "Exception raised in %s. Exception: %s", func_name, str(e)
                )
                raise e

        return wrapper

    return decorate_func(_func)
