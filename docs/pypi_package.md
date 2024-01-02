# Using the CAS PyPI Package

The  Cell Annotation Schema PyPI package is available at https://pypi.org/project/cell-annotation-schema/

Python package can be used as a library to validate CAS json files and implement CAS schema extensions:

## Read Schemas

CAS python package includes bundled schema files (`general_schema.json`, `BICAN_schema.json` and `CAP_schema.json`) located at `cas_schema/schemas`

To access these bundled JSON files, you can utilize the `importlib` package as shown below:

```python
import json
from importlib import resources
from cas_schema import schemas

schema_file = (resources.files(schemas) / "BICAN_schema.json")
with schema_file.open("rt") as f:
    BICAN_schema = json.loads(f.read())
```

## Validate

The package allows for the validation of CAS data instances against schema files using the `schema_validator.validate` function. Here's an example:

```python
from cas_schema import schema_validator

result = schema_validator.validate(BICAN_schema, "BICAN_schema.json", '/path/to/my_cas_instance.json')
```

The `validate` function checks if all the test files provided are valid according to the schema. If any validation errors occur, they are logged.

_Function:_ `schema_validator.validate`

    Validates all json files located in the test path with the given schema.
        Parameters:
            schema: json schema object
            schema_name: name (or path) of the schema. Used for reporting purposes only.
            test_path: path to the data files. If path is a folder, validates all json files inside. If path is a json file,
            validates it.
        Returns:
            'True' if all test files are valid, 'False' otherwise. Logs the validation errors if any.

## Merge Schemas

For details regarding the schema extension logic, refer to the information provided in [schema-extension.md](schema-extension.md).

To merge base schemas into the current schema and obtain a merged JSON schema, you can use the `schema_manager.load` operation, provided that a JSON schema follows the schema extension logic. Here's an example:

```python
from cas_schema import schema_manager

schema_json = schema_manager.load('/path/to/my_schema.json')
```

The `load` function retrieves the schema JSON object from the specified path and, in addition to standard schema loading, recursively merges declared base schemas based on the specified import strategy (extend/override). The default strategy is extension.

_Function:_ `schema_manager.load`

    Loads the schema json object from the given path. In addition to vanilla schema loading, recursively merges declared base schemas according to the specified import strategy (extend/override).
        Parameters:
            path: file path or web url of the schema
            strategy: (optional) schema merge strategy (extend/override). Default strategy is extension
            referrer_path: (optional) path of the referring schema. Used for resolving the relative paths.
            catalog_file: catalog file to locally resolve web urls. This is useful for local development and testing. Paths in the catalog file are relative to the catalog file itself.
        Returns:
            merged schema
