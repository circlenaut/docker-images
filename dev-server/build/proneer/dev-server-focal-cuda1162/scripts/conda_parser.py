"""
Derived from: https://github.com/librariesio/conda-parser
"""

import os
import sys
import re
import typing
import yaml
import logging
import coloredlogs
from yaml                    import CLoader
from conda.api               import Solver
from conda.exceptions        import ResolvePackageNotFound
from conda.models.match_spec import MatchSpec

### Enable logging
logging.basicConfig(
    format='%(asctime)s [%(levelname)s] %(message)s', 
    level=logging.INFO, 
    stream=sys.stdout)

log = logging.getLogger(__name__)

# Set log level
verbosity = os.getenv("LOG_VERBOSITY", "INFO")
log.setLevel(verbosity)
# Setup colored console logs
coloredlogs.install(fmt='%(asctime)s [%(levelname)s] %(message)s', level=verbosity, logger=log)

SUPPORTED_CHANNELS = {"defaults", "nodefaults", "anaconda", "conda-forge"}
SUPPORTED_EXTENSIONS = {
    ".yml",
    ".yaml",
    ".lock",
}  # Only file extensions that are allowed
FILTER_KEYS = {
    "name",
    "dependencies",
    "channels",
    "prefix",
}  # What keys we want back from the environment file


def _get_extension(filename: str) -> str:
    _, extension = os.path.splitext(filename)
    return extension.lower()


def supported_filename(filename: str) -> bool:
    return _get_extension(filename) in SUPPORTED_EXTENSIONS


def is_lock(filename: str) -> bool:
    return _get_extension(filename) == ".lock"


def read_environment(environment_file: str) -> dict:
    """
    Loads the file into yaml and returns the keys that we care about.
        example: ignores `prefix:` settings in environment.yml
    """
    environment = yaml.load(environment_file, Loader=CLoader)
    return {k: v for k, v in environment.items() if k in FILTER_KEYS}


def clean_out_pip(specs: list) -> list:
    """ Not supporting pip for now """
    return [spec for spec in specs if isinstance(spec, str)]


def clean_channels(channels: list) -> list:
    """
    Grab channels from the environment file, but remove any that
    aren't in the supported channels list.
    """
    channels_left = [channel for channel in channels if channel in SUPPORTED_CHANNELS]

    if "nodefaults" not in channels_left and "defaults" not in channels_left:
        channels_left += ["defaults"]
    return channels_left


def match_specs(specs: list) -> list:
    """
    Specs come in in a variety of formats, get the name and version back,
    this removes the build parameter, and always returns a dict of name/requirement
    """
    _specs = []
    for dep in specs:
        spec = MatchSpec(dep)
        _specs.append({"name": str(spec.name), "requirement": str(spec.version or "")})
    return _specs


def parse_environment(
    filename: str, environment_file: str, force_solve: bool = False
) -> dict:
    """
        Loads a file, checks some common error conditions, tries its best
    to see if it is an actual Conda environment.yml file, and if it is,
    it will return a dictionary of a list of the manifest, lockfile, and channels.

    returns
        - dict of "error": "message"
        or
        - dict of "lockfile", "manifest", "channels"
    """
    # we need the `file` field
    if not environment_file:
        return {"error": "No `file` provided."}
    # file must be in .yaml or .yml format
    if not filename or not supported_filename(filename):
        return {"error": "Please provide a `.yml` or `.yaml` environment file"}
    # Parse the file
    try:
        environment = read_environment(environment_file)
    except yaml.YAMLError as exc:
        return {"error": f"YAML parsing error in environment file: {exc}"}
    if not environment.get("dependencies"):
        return {"error": f"No `dependencies:` in your {filename}"}
    # Ignore pip, and pin to specific format
    manifest = match_specs(clean_out_pip(environment["dependencies"]))
    environment["dependencies"] = manifest

    environment["channels"] = clean_channels(environment.get("channels", ["defaults"]))
    if force_solve or is_lock(filename):
        lockfile, bad_specs = solve_environment(environment)
        # Sort the lockfile
        lockfile = sorted(lockfile, key=lambda i: i.get("name", ""))
    else:
        lockfile = None
        bad_specs = []
    output = {
        "name" : environment["name"],
        "manifest": sorted(manifest, key=lambda i: i.get("name", "")),
        "lockfile": lockfile,
        "channels": environment["channels"],
        "bad_specs": sorted(bad_specs),
    }
    return output


def solve_environment(environment: dict) -> typing.Tuple[list, list]:
    """
    Using the Conda API, Solve an environment, get back all
    of the dependencies.

    returns a list of {"name": name, "requirement": requirement} values.
    """
    prefix = environment.get("prefix", ".")
    channels = environment["channels"]
    specs = [
        f"{spec['name']} {spec.get('requirement', '')}".rstrip()
        for spec in environment["dependencies"]
    ]

    bad_specs = []
    try:
        dependencies = Solver(prefix, channels, specs_to_add=specs).solve_final_state()
    except ResolvePackageNotFound as e:
        ok_specs, bad_specs = rigidly_parse_error_message(e.message, specs)
        dependencies = Solver(
            prefix, channels, specs_to_add=ok_specs
        ).solve_final_state()

    return (
        [{"name": dep["name"], "requirement": dep["version"]} for dep in dependencies],
        bad_specs,
    )


def rigidly_parse_error_message(message: str, specs: list) -> typing.Tuple[list, list]:
    """
    The error message, as generated by conda.exceptions.ResolvePackageNotFound, adds
    some spaces, a dash and a space (yaml list), rather than parse the yaml, just strip off
    those bits and make a difference list
    """
    message = message.split("\n")  # split by newlines
    bads = set(bad.lstrip("  - ") for bad in message if bad)

    good = set(specs) - bads

    return list(good), list(bads)