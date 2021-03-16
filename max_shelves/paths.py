# Import built-in modules
from collections import OrderedDict
from contextlib import contextmanager
import glob
import json
import os
import sys


def read_json(file_path):
    with open(file_path, "r") as file_obj:
        return json.load(file_obj)


def get_default_path():
    return os.path.join(os.path.dirname(__file__), "tools")


def get_script_search_paths():
    try:
        paths = os.getenv("MAX_SHELVES_PATH").split(os.path.pathsep)
    except AttributeError:
        paths = []
    paths.insert(0, get_default_path())
    return paths


def resolve_paths(paths):
    tools = []
    for path in paths:
        tools.extend(glob.iglob(os.path.join(path, "*", "*", "tool.json")))
    return tools


def resolve_tools(paths):
    data = OrderedDict()
    for tool in paths:
        tab = os.path.basename(os.path.dirname(os.path.dirname(tool)))
        tool_meta = patch_meta(tool)
        items = data.get(tab) or []
        items.append(tool_meta)
        data[tab] = items
    return data


def patch_meta(tool):
    root = os.path.dirname(tool)
    tool_meta = read_json(tool)
    tool_meta["root"] = root
    script = tool_meta["main"]
    icon = tool_meta["icon"]
    if not os.path.isfile(script):
        script = os.path.join(root, script)
    if not os.path.isfile(icon):
        icon = os.path.join(root, icon)
    tool_meta["icon"] = icon
    tool_meta["script"] = script.replace("\\", "/")
    return tool_meta


@contextmanager
def append_to_python_path(script):
    """Add to ``sys.path``, and revert on scope exit.

    Args:
        script (str): The absolute path of the script file.

    """
    script_root = os.path.dirname(script)
    original_syspath = sys.path[:]
    sys.path.append(script_root)
    try:
        yield
    finally:
        sys.path = original_syspath
