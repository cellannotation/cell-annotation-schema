from schema_merger import OverrideStrategy, ExtensionStrategy
from json_utils import get_json, get_absolute_path


merge_strategy = OverrideStrategy()


def load(path: str, strategy=merge_strategy, referrer_path=None) -> dict:
    """
    Loads the schema json object from the given path. In addition to vanilla schema loading, recursively merges declared
     base schemas according to the declared import strategy (extend/override)
    :param path: file path of the schema
    :param strategy: (optional) schema merge strategy (extend/override)
    :param referrer_path: (optional) path of the referring schema. Used for resolving the relative paths.
    """
    # TODO add cyclic import prevention logic
    schema = get_json(path, referrer_path)

    merged_base = None
    if "allOf" in schema:
        for base_schema_declaration in schema["allOf"]:
            base_ref = base_schema_declaration["$ref"]
            abs_path = get_absolute_path(path, referrer_path)
            if merged_base is None:
                merged_base = load(base_ref, strategy, abs_path)
            else:
                merged_base = strategy.merge(merged_base, load(base_ref, strategy, abs_path))

    if merged_base is not None:
        schema = strategy.merge(merged_base, schema)
        del schema['allOf']

    return schema
