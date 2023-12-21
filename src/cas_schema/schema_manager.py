import os
import json

from cas_schema.schema_merger import OverrideStrategy, ExtensionStrategy
from cas_schema.json_utils import get_json, resolve_path


BICAN_SCHEMA = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../../BICAN_extension.json")
CAP_SCHEMA = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../../CAP_extension.json")

BICAN_ASSET = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../../BICAN_schema.json")
CAP_ASSET = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../../CAP_schema.json")

merge_strategy = ExtensionStrategy()


def load(path: str, strategy=merge_strategy, referrer_path=None, catalog_file=None) -> dict:
    """
    Loads the schema json object from the given path. In addition to vanilla schema loading, recursively merges declared
     base schemas according to the specified import strategy (extend/override).
    :param path: file path or web url of the schema
    :param strategy: (optional) schema merge strategy (extend/override). Default strategy is extension
    :param referrer_path: (optional) path of the referring schema. Used for resolving the relative paths.
    :param catalog_file: catalog file to locally resolve web urls. This is useful for local development and testing.
    Paths in the catalog file are relative to the catalog file itself.
    :return: merged schema
    """
    # TODO add cyclic import prevention logic
    schema = get_json(path, referrer_path, catalog_file)

    merged_base = None
    if "allOf" in schema:
        for base_schema_declaration in schema["allOf"]:
            base_ref = base_schema_declaration["$ref"]
            abs_path = resolve_path(path, referrer_path, catalog_file)
            if merged_base is None:
                merged_base = load(base_ref, strategy, abs_path, catalog_file)
            else:
                merged_base = strategy.merge(merged_base, load(base_ref, strategy, abs_path, catalog_file))

    if merged_base is not None:
        schema = strategy.merge(merged_base, schema)
        del schema['allOf']

    return schema


def generate_release_assets():
    """
    Generates BICAN and CAP release assets in the project root folder.
    These assets are uploaded to the related release by GitHub actions.
    """
    bican_schema = load(BICAN_SCHEMA)
    with open(BICAN_ASSET, "w") as outfile:
        outfile.write(json.dumps(bican_schema, indent=2))

    cap_schema = load(CAP_SCHEMA)
    with open(CAP_ASSET, "w") as outfile:
        outfile.write(json.dumps(cap_schema, indent=2))


if __name__ == "__main__":
    generate_release_assets()
