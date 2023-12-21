import glob
import sys
import os
import warnings

from pathlib import Path
from typing import List

from cas_schema.json_utils import get_json_from_file
from cas_schema.schema_manager import load


from jsonschema import Draft202012Validator, RefResolver, SchemaError


warnings.filterwarnings("always")


def validate(schema, schema_name, test_path):
    """
    Validates all json files located in the test path with the given schema.
    Parameters:
        schema: json schema object
        schema_name: name (or path) of the schema. Used for reporting purposes only.
        test_path: path to the data files. If path is a folder, validates all json files inside. If path is a json file,
        validates it.
    Returns:
        'True' if all test files are valid, 'False' otherwise. Logs the validation errors if any.
    """
    sv = get_validator(schema, schema_name)
    if os.path.isdir(test_path):
        test_files = glob.glob(pathname=test_path + "/*.json")
    else:
        if Path(test_path).suffix == ".json":
            test_files = [test_path]
        else:
            raise Exception("Test file extension not supported: {}".format(test_path))
    validation_status: List[bool] = []
    print("Found %s test files in %s" % (str(len(test_files)), test_path))
    for instance_file in test_files:
        i = get_json_from_file(instance_file)
        print("Testing: %s" % instance_file)
        validation_status.append(validate_file(sv, i))
    return False not in validation_status


def get_validator(schema, filename, base_uri=""):
    """Load schema from JSON file;
    Check whether it's a valid schema;
    Return a Draft4Validator object.
    Optionally specify a base URI for relative path
    resolution of JSON pointers (This is especially useful
    for local resolution via base_uri of form file://{some_path}/)
    """
    try:
        # Check schema via class method call. Works, despite IDE complaining
        # However, it appears that this doesn't catch every schema issue.
        Draft202012Validator.check_schema(schema)
        print("%s is a valid JSON schema" % filename)
    except SchemaError:
        raise
    if base_uri:
        resolver = RefResolver(base_uri=base_uri, referrer=filename)
    else:
        resolver = None
    return Draft202012Validator(schema=schema, resolver=resolver)


def get_schema(filename):
    """
    Reads the json schema from the given location
    """
    catalog_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "catalog.yaml")
    schema = load(filename, catalog_file=catalog_file_path)
    return schema


def validate_file(validator, instance):
    """Validate an instance of a schema and report errors."""
    if validator.is_valid(instance):
        print("Validation Passes")
        return True
    else:
        es = validator.iter_errors(instance)
        recurse_through_errors(es)
        print("Validation Fails")
        return False


def recurse_through_errors(es, level=0):
    """Recurse through errors posting message
    and schema path until context is empty"""
    for e in es:
        warnings.warn(
            "***" * level
            + " subschema level "
            + str(level)
            + "\t".join([str(e.message), "Path to error:" + str(e.absolute_schema_path)])
            + "\n"
        )
        if e.context:
            level += 1
            recurse_through_errors(e.context, level=level)


def run_validator(path_to_schema_dir, schema_file, path_to_test_dir):
    """Tests all instances in a test_folder against a single schema.
    Assumes all schema files in single dir.
    Assumes all *.json files in the test_dir should validate against the schema.
       * path_to_schema_dir:  Absolute or relative path to schema dir
       * schema_file: schema file name
       * test_dir: path to test directory (absolute or local to schema dir)
    """
    # Getting script directory, schema directory and test directory
    script_folder = Path(os.path.dirname(os.path.realpath(__file__)))
    schema_dir = Path(os.path.dirname(path_to_schema_dir))
    test_path = os.path.join(script_folder, os.path.dirname(path_to_test_dir))
    if not os.path.exists(os.path.join(script_folder, schema_dir)):
        raise Exception("Please provide valid path_to_schema_dir")
    if not os.path.exists(test_path):
        raise Exception("Please provide valid path_to_test_dir")
    else:
        schema_file_path = os.path.join(script_folder, schema_dir, schema_file)
        schema = get_schema(schema_file_path)

        result = validate(schema, schema_file_path, test_path)
        if not result:
            raise Exception("Validation Failed")


if __name__ == "__main__":
    run_validator(
        path_to_schema_dir="../../", schema_file="general_schema.json", path_to_test_dir="../../examples/"
    )
    run_validator(
        path_to_schema_dir="../../", schema_file="BICAN_extension.json", path_to_test_dir="../../examples/BICAN_schema_specific_examples/"
    )
    run_validator(
        path_to_schema_dir="../../", schema_file="CAP_extension.json", path_to_test_dir="../../examples/CAP_schema_specific_files/"
        # Need to simplify names
    )
