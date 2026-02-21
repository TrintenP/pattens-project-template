# pattens-project-template

# About the Project
This repo exists as a base Python template that can be used to kickstart a new project and have core functionality available out the gate.

# Getting Started
## Prerequisites
1. Python 3.13+
    `https://www.python.org/downloads/release/python-3130/`
2. UV package manager
    `pip install uv`
## Installation
1. Clone the GIT repo
    - `git clone https://github.com/TrintenP/pattens-project-template.git`
2. Change into cloned repo
    - `cd pattens-project-template`
3. Create a virtual environment
    - `uv venv --python 3.13`
4. Activate virtual environment
    - `.venv\Scripts\activate`
5. Update virtual environment
    - `uv sync`
6. Run commands (See ['Usage'](#usage) Section)

# Usage

## General Usage
This project will create a set of entry points that can be used in the console.

`ppt`: Will parse command line for arguements.
    - Arguments:
        - TBA

## Development Usage
This section is to provide additional information about some already included quality of life functions added in the template.

### Commands:
- `run-docs`: Will automatically parse doc-strings to generate, and open, a local copy of documentation of the code. 
- `run-tests [--disablecov | ]`: Run the test suit, defaults to generating a local coverage report and opening the report.
- `run-ci`: Will locally run the CI pipeline to ensure proper linting, tests pass, etc.
- `version-bump --vbump <major|minor|patch>`: QoL script that automatically bumps the version of the code. Defaults to patch.

### Useful UV commands
- `uv add <package>`: Add in specified package to the environment
- `uv remove <package>`: Remove specified package from the environment
- `uv build --no-sources`: Build the project


# License
Distributed under the MIT License. See `License.txt` for more information.

# Contact
Trinten Patten - trintenmpatten@gmail.com
Project Link: https://github.com/TrintenP/pattens-project-template

# Acknowledgments
Some resources that have been useful for the creation of this template are:

- [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)
- [Semantic Versioning](https://semver.org/spec/v2.0.0.html)
- [GitHub Pages](https://pages.github.com)
- [Img Shields](https://shields.io)
- [Choose an Open Source License](https://choosealicense.com)