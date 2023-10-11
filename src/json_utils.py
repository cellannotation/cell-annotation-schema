import os
import json
import warnings

from urllib.request import urlopen


def get_json(path, referrer_path=None):
    """
    Reads json from the given path. Path can be a relative or absolute file path or a web URL.
    :param path: path of the json.
    :param referrer_path: (optional) absolute path of the referring schema. Used for resolving the relative paths.
    """
    if is_web_url(path):
        return get_json_from_url(path)
    else:
        return get_json_from_file(get_absolute_path(path, referrer_path))


def get_absolute_path(path_to_resolve, referrer_abs_path):
    """
    Creates an absolute path from the given path relative to the referrer absolute path
    :param path_to_resolve: relative path to resolve
    :param referrer_abs_path: absolute path of the referrer
    :return absolute path
    """
    if is_web_url(path_to_resolve) or referrer_abs_path is None:
        return path_to_resolve

    if is_web_url(referrer_abs_path):
        warnings.warn("Schema read from the web ({}) cannot import from relative path ({})."
                      .format(referrer_abs_path, path_to_resolve))

    if os.path.isfile(path_to_resolve):
        return path_to_resolve
    else:
        # process relative path
        referrer_folder = os.path.dirname(os.path.abspath(referrer_abs_path))
        abs_path = os.path.join(referrer_folder, path_to_resolve)
        if os.path.isfile(abs_path):
            return abs_path
        else:
            warnings.warn("File not found: " + path_to_resolve)




def is_web_url(path):
    return str(path).startswith("http://") or str(path).startswith("https://")


def get_json_from_url(url):
    """Loads JSOn from web URL."""
    return json.loads(urlopen(url).read())


def get_json_from_file(filename):
    """Loads JSON from a file."""
    try:
        with open(filename, "r") as f:
            fc = f.read()
        return json.loads(fc)
    except FileNotFoundError:
        warnings.warn("File not found: " + filename)
    except IOError as exc:
        warnings.warn("I/O error while opening " + filename + ": " + str(exc))
    except json.JSONDecodeError as exc:
        warnings.warn("Failed to parse JSON in " + filename + ": " + str(exc))