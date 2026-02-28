import pathlib

from sphinx_pyproject import SphinxConfig

from ppt import __version__ as project_version

filepath = pathlib.Path(__file__).parents[2] / "pyproject.toml"

# Overriding config value due to not dynamic version unsupported.
config = SphinxConfig(
    filepath, globalns=globals(), config_overrides={"version": project_version}
)
