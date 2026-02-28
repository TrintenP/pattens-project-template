"""Contains general utility functions."""

import logging
import os
import pathlib

import ppt
from ppt.util.log_utils import enable_logging
from ppt.util.parsing import search_file

logger = logging.getLogger(__name__)


@enable_logging
def return_true() -> bool:
    """To be used for testing imports.

    :return: Will always return True
    :rtype: bool
    """
    return True


@enable_logging
def raise_error() -> None:
    """To be used to test error catching. Raises Value Error."""
    raise ValueError


@enable_logging
def bump_version(part: str, testing_mode: bool = False) -> str:
    """Helper function to quickly modify module versioning.

    Increments either the major, minor, or patch version of the module.

    :param part: Which part of the version to modify.
    :type part: str
    :param testing_mode: If True loads in test init file, defaults to False
    :type testing_mode: bool, optional
    :return: Returns updated version.
    :rtype: str
    """
    part = part.lower()
    version_parts = ["major", "minor", "patch"]

    if part not in version_parts:
        version = ppt.__version__
        logger.error("Unkown part: %s. Version is still %s", part, version)
        return version

    part_index = version_parts.index(part)

    parent_paths = pathlib.Path(__file__).parents
    real_init = parent_paths[1] / "__init__.py"
    mock_init = parent_paths[2] / "tests" / "data" / "mock_init.txt"
    version_file = real_init if not testing_mode else mock_init

    version_index = search_file(version_file, "__version__")

    if version_index == "NA":
        logging.error(
            "Could not find __vesrsion__ attribute in %s, exiting early.",
            pathlib.Path(version_file).as_posix(),
        )
        # Return value for testing purposes
        return "NA"

    with open(version_file, "r") as fin:
        file_contents = fin.readlines()

        # Line Format: __version__ = "x.x.x"
        version_line = file_contents[version_index]
        version_vals = [c for c in version_line if c.isnumeric()]

    version_vals[part_index] += 1
    new_version: str = ".".join(version_vals)
    new_line = f"__version__ = '{new_version}'{os.linesep}"

    logger.debug("Old Version: %s", version_line.strip())
    logger.debug("New Version: %s", new_line.strip())

    insert_into_file(version_file, new_line, version_index)

    return new_version


@enable_logging
def insert_into_file(
    filepath: pathlib.Path, to_be_inserted: str, index: int
) -> None:
    """Helper function to insert a value at a given location in a file.

    :param filepath: File to be modified.
    :type filepath: pathlib.Path
    :param to_be_inserted: Line to be inserted into the file.
    :type to_be_inserted: str
    :param index: Where in the file to insert the new line.
    :type index: int
    """
    with open(filepath, "r") as fin:
        content = fin.readlines()

    content[index] = to_be_inserted

    with open(filepath, "w") as fout:
        fout.writelines(content)
