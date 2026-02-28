"""Contains functions that will handle different types of parsing."""

import argparse
import logging
import pathlib
import sys

from ppt.util.log_utils import enable_logging

logger = logging.getLogger(__name__)


@enable_logging
def parse_input(arg_list: list | None = None) -> argparse.Namespace:
    """Parses inputs from command line, and creates a namespace for them.

    :param arg_list: CMD-styled input of strings, defaults to sys.argv[1:]
    :type arg_list: list | None, optional
    :return: Namespace that contains all parse inputs for given arguements.
    :rtype: argparse.Namespace
    """
    if arg_list is None:
        arg_list = sys.argv[1:]

    parser = argparse.ArgumentParser(description="Parse inputs from cli.")

    # Enable dev mode for more robust logging
    parser.add_argument("--dev", action="store_true", help="Enables dev mode.")

    parser.add_argument(
        "-v",
        "--vbump",
        nargs="?",  # 0/1 arguments
        const="patch",  # Default is patch if no args
        help="Increment version number.",
    )

    parser.add_argument(
        "--disablecov",
        action="store_true",
        help="Disables coverage report generation.",
    )

    args = parser.parse_args(arg_list)
    logger.debug("Args read in are: %s", args)

    return args


@enable_logging
def search_file(filepath: pathlib.Path, search_str: str) -> int:
    """Parses the given file for first instance of search string.

    :param filepath: The file to be searched.
    :type filepath: pathlib.Path
    :param search_str: The string to search each line for.
    :type search_str: str
    :return: Line index of search string. -1 if search string not found.
    :rtype: int
    """

    index = -1

    try:
        with open(filepath, "r") as fin:
            for idx, line in enumerate(fin):
                if search_str.lower() in line.lower():
                    index = idx
                    break
    except FileNotFoundError:
        logging.error("Could not find file at %s", filepath.resolve())

    return index
