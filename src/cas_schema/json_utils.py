import os
import json
import warnings

from urllib.request import urlopen
from ruamel.yaml import YAML

# cache of catalog files for performance reasons
catalog_cache = dict()


def get_json(path, referrer_path=None, catalog_file=None):
    """
    Reads json from the given path. Path can be a relative or absolute file path or a web URL.
    :param path: path of the json.
    :param referrer_path: (optional) absolute path of the referring schema. Used for resolving the relative paths.
    :param catalog_file: catalog file to locally resolve web urls. This is useful for local development and testing.
    Paths in the catalog file are relative to the catalog file itself.
    """
    resolved_path = resolve_path(path, referrer_path, catalog_file)
    if is_web_url(resolved_path):
        return get_json_from_url(resolved_path)
    else:
        return get_json_from_file(resolved_path)


def resolve_path(path_to_resolve, referrer_abs_path, catalog_file):
    """
    Resolves the give path to its actual location. If given path is already an absolute path, returns it directly.
    If path is relative, resolves it based on referrer's path.
    If a catalog file is provided, resolves web urls accordingly.
    :param path_to_resolve: relative path to resolve
    :param referrer_abs_path: absolute path of the referrer
    :param catalog_file: catalog file to locally resolve web urls. This is useful for local development and testing.
    Paths in the catalog file are relative to the catalog file itself.
    :return: absolute path
    """
    if is_web_url(path_to_resolve):
        return resolve_via_catalog(path_to_resolve, catalog_file)

    if referrer_abs_path is None:
        return path_to_resolve

    if is_web_url(referrer_abs_path):
        warnings.warn("Schema read from the web ({}) cannot import from relative path ({})."
                      .format(referrer_abs_path, path_to_resolve))

    if os.path.isabs(path_to_resolve):
        return path_to_resolve
    else:
        # process relative path
        referrer_folder = os.path.dirname(os.path.abspath(referrer_abs_path))
        abs_path = os.path.join(referrer_folder, path_to_resolve)
        if os.path.isfile(abs_path):
            return abs_path
        else:
            warnings.warn("File not found: '{}' at its resolved location: '{}'".format(path_to_resolve, abs_path))


def resolve_via_catalog(web_url, catalog_file):
    """
    Tries to resolve given web url from the catalog. If cannot find in the catalog, returns as is.
    """
    if catalog_file is not None:
        catalog_obj = read_catalog(catalog_file)
        if web_url in catalog_obj:
            relative_path = catalog_obj[web_url]
            return resolve_path(relative_path, catalog_file, None)
    return web_url


def read_catalog(catalog_file):
    """
    Reads the catalog file from the given path and caches it. If already in the cache, returns the cached obj.
    :param catalog_file: path of the catalog file
    :return: catalog object
    """
    if catalog_file in catalog_cache:
        catalog_obj = catalog_cache[catalog_file]
    else:
        ryaml = YAML(typ='safe')
        with open(catalog_file) as stream:
            catalog_obj = ryaml.load(stream)
            catalog_cache[catalog_file] = catalog_obj
    return catalog_obj


def is_web_url(path):
    """
    Checks if the given path is a web URL.
    :param path: path reference to check
    :return: True if a web URL, False otherwise
    """
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