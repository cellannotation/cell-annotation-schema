# Extending Schemas

This project introduces a schema extension mechanism. 

Extension schemas can now import base schemas using the `allOf` keyword, either through an absolute URL like:

```json
"allOf": [
      {"$ref": "https://raw.githubusercontent.com/cellannotation/cell-annotation-schema/main/general_schema.json" }
    ],
```
Or, you can use relative paths for referencing the base schema:
```json
"allOf": [
      {"$ref": "./general_schema.json" }
    ],
```
These paths are relative to the extension schema file's location.

To make use of these schema extension capabilities `schema_manager.load` should be used instead of `json.loads` while reading the schema files. `schema_manager.load` operation will merge all properties of the imported schema to the current schema and will resolve any conflicts.

Schema merging operation is a recursive operation and supports importing multiple base schemas. Even base schemas can import other schemas.

_NOTE: Currently we don`t have mechanisms to detect and prevent cyclic imports. So, please make sure you don't cause one._

## Conflict resolution

A conflict occurs when extension schema re-declares a base property with a different configuration. Such as, for a given base property:

```json
    "age": {
      "description": "Age in years which must be equal to or greater than zero.",
      "type": "integer",
      "minimum": 0
    }
```
if extension declares `age` with different settings, a conflict occurs.
```json
    "age": {
      "type": "string",
      "description": "Age of the person."
    }
```
By default, both of these should be satisfied to have a valid json data, which is impossible.

To overcome conflicts, we provide two conflict resolution strategies. These strategies ensure that extension schemas work seamlessly with the base schema, with the default strategy being the "ExtensionStrategy."

- **ExtensionStrategy**: In this mode, extension schema can introduce new properties without overriding the base schema. In the event of a conflict, the declarations from the base schema take precedence, and `required` property declarations are merged.
- **OverrideStrategy**: In this strategy, extension schemas have the flexibility to both add new properties and override existing properties in the base schema. When conflicts arise, the declarations from the extension schema will override those in the base schema, while `required` property declarations will be sourced from the extending schema.

If there are not any conflicts, these two strategies produces the same output.

## Catalog files

While extension schemas commonly should reference to base schemas via web URLs (or PURLs), catalog files can be invaluable for development and testing purposes. They enable the redirection of web URLs to local schema files, facilitating a smooth development and testing workflow.

An example catalog file is located at [src/catalog.yaml](src/catalog.yaml)

```yaml
https://raw.githubusercontent.com/cellannotation/cell-annotation-schema/main/general_schema.json: ../general_schema.json
```

Pointed local file paths are relative to the location of the `catalog.yaml` file itself. Hence, in this example, it is relative to `{root_folder}/src/catalog.yaml` which resolves to `{root_folder}/src/catalog.yaml`.

A basic caching mechanism added for catalog files to prevent repetitive file read operations and accordingly increase performance.
