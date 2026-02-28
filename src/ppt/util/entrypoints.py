"""
Contains different command line entry points for the module.
"""

import logging
import os
import pathlib
import subprocess
import webbrowser

from ppt.util import general
from ppt.util.log_utils import setup_logging
from ppt.util.parsing import parse_input

logger = logging.getLogger(__name__)


def generate_documentation() -> None:
    """Entrypoint used to easily generate auto-generated documentation."""

    setup_logging(log_level=logging.DEBUG)

    root = pathlib.Path(__file__).parents[3]
    docs_folder = root / "docs"

    os.chdir(docs_folder)
    make_location = str(pathlib.Path("./make.bat").resolve())

    gen_args = ["sphinx-apidoc", "-o", "./source", "../src/ppt"]
    devnull = subprocess.DEVNULL

    # Create .rst files for Sphinx
    gen_rtn_code = subprocess.call(gen_args, stdout=devnull)  # noqa: S603

    logger.debug("Generation returned: %s", gen_rtn_code)

    make_clean_args = [make_location, "clean"]
    make_run_args = [make_location, "html"]

    logger.info("Removing all existing docs under build.")
    clean_rtn_code = subprocess.call(make_clean_args, stdout=devnull)  # noqa: S603
    logger.debug("Make Clean returned: %s", clean_rtn_code)

    logger.info("Creating new documentation.")
    make_rtn_code = subprocess.call(make_run_args, stdout=devnull)  # noqa: S603
    logger.debug("Make html returned: %s", make_rtn_code)

    doc_location = pathlib.Path("./build/html/index.html").resolve()
    logger.info("Documentation is available at: %s", doc_location.as_posix())
    webbrowser.open(str(doc_location), 1)


def run_testing(arg_list: list | None = None) -> None:
    """Runs the test suite of the program, and can generate a coverage file.

    :param arg_list: CMD-styled input of strings, defaults to sys.argv[1:]
    :type arg_list: list | None, optional
    """

    args = parse_input(arg_list)

    coverage_commands = ["coverage", "run", "-m", "pytest"]

    if args.disablecov:
        subprocess.call(coverage_commands)  # noqa: S603
        return

    report_gen_commands = ["coverage", "html", "-d", "coverage_report"]
    subprocess.call(report_gen_commands)  # noqa: S603

    report_loc = pathlib.Path().cwd() / "coverage_report" / "index.html"

    webbrowser.open(str(report_loc), 1)


def run_local_ci() -> bool:
    """Runs a local version of the CI pipeline.

    :return: Return True on pass of CI pipeline, else Fasle.
    :rtype: bool
    """

    setup_logging(log_level=logging.DEBUG)
    return_val = True
    devnull = subprocess.DEVNULL

    # Format / Lint
    ruff_commands = ["ruff", "format"]

    # Type Checking
    ty_commands = ["ty", "check"]

    # Testing
    test_commands = ["pytest"]

    list_of_commands = [
        (ruff_commands, "format and security checks"),
        (ty_commands, "type checks"),
        (test_commands, "tests"),
    ]

    try:
        for command_set, print_statement in list_of_commands:
            logger.debug("Running %s now!", print_statement)
            stat = subprocess.call(command_set, stderr=devnull, stdout=devnull)  # noqa: S603

            if stat == 0:
                logger.debug("%s was successfull!", print_statement)
            else:
                logger.debug("%s failed!", print_statement)
                return_val = False
    except Exception as e:
        logger.exception("%s occurred during testing. Exiting early", e)
        return False

    if not return_val:
        logger.info("A testing step has failed, please check logs.")

    return return_val


def run_ppt(arg_list: list | None = None) -> None:
    """Runs the tool in general command line mode.

    :param arg_list: CMD-styled input of strings, defaults to sys.argv[1:]
    :type arg_list: list | None, optional
    """

    args = parse_input(arg_list)

    log_level = logging.DEBUG if args.dev else logging.WARNING
    setup_logging(log_level=log_level)
    logger.info("Successfully loaded in the following args %s", args)

    if args.vbump:
        new_version = general.bump_version(args.vbump)
        logger.info("Version updated to: %s", new_version)
