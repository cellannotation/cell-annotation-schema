import unittest
import os
import json

from schema_manager import load
from schema_merger import OverrideStrategy, ExtensionStrategy

GENERAL_SCHEMA = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../../general_schema.json")
BICAN_SCHEMA = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../../BICAN_extension.json")


class SchemaManagerTests(unittest.TestCase):

    def test_loading_general_schema(self):
        schema = load(GENERAL_SCHEMA)
        print(json.dumps(schema, indent=2))

        self.assertIn("title", schema)
        self.assertEqual("General Cell Annotation Open Standard", schema["title"])

        self.assertIn("Annotation", schema["definitions"])
        self.assertIn("cellannotation_setname", schema["definitions"]["Annotation"]["properties"])

        self.assertNotIn("cell_set_accession", schema["definitions"]["Annotation"]["properties"])
        self.assertNotIn("parent_cell_set_accessions", schema["definitions"]["Annotation"]["properties"])

    def test_loading_BICAN_schema(self):
        schema = load(BICAN_SCHEMA)
        print(json.dumps(schema, indent=2))

        self.assertIn("title", schema)
        self.assertEqual("General Cell Annotation Open Standard", schema["title"])

        # from base
        self.assertIn("automated_annotation", schema["definitions"])
        # from bican
        self.assertIn("Annotation_transfer", schema["definitions"])

        # merged Annotation
        self.assertIn("Annotation", schema["definitions"])
        self.assertIn("cellannotation_setname", schema["definitions"]["Annotation"]["properties"])
        self.assertIn("cell_set_accession", schema["definitions"]["Annotation"]["properties"])
        self.assertIn("parent_cell_set_accessions", schema["definitions"]["Annotation"]["properties"])

        # merged cellannotation_setname_metadata
        self.assertIn("cellannotation_setname_metadata", schema["definitions"])
        self.assertIn("rank", schema["definitions"]["cellannotation_setname_metadata"]["properties"])
        self.assertIn("name", schema["definitions"]["cellannotation_setname_metadata"]["properties"])

        self.assertNotIn("allOf", schema)

    def test_import_relative_path(self):
        test_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "./test_data/BICAN_extension_relative.json")
        schema = load(test_file)
        print(json.dumps(schema, indent=2))

        self.assertIn("title", schema)
        self.assertEqual("General Cell Annotation Open Standard", schema["title"])

        # from base
        self.assertIn("automated_annotation", schema["definitions"])
        # from bican
        self.assertIn("Annotation_transfer", schema["definitions"])

        # merged Annotation
        self.assertIn("Annotation", schema["definitions"])
        self.assertIn("cellannotation_setname", schema["definitions"]["Annotation"]["properties"])
        self.assertIn("cell_set_accession", schema["definitions"]["Annotation"]["properties"])
        self.assertIn("parent_cell_set_accessions", schema["definitions"]["Annotation"]["properties"])

    def test_recursive_loading(self):
        test_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "./test_data/extension_2.json")
        schema = load(test_file)

        # from base_schema.json
        self.assertIn("title", schema)
        self.assertEqual("Person", schema["title"])
        self.assertIn("firstName", schema["properties"])

        # from extension_1.json
        self.assertIn("occupation", schema["properties"])

        # from extension_2.json
        self.assertIn("idNumber", schema["properties"])

    def test_overriding_strategy(self):
        test_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "./test_data/extension_2.json")
        schema = load(test_file, OverrideStrategy())

        # handle conflict
        self.assertEqual("double", schema["properties"]["age"]["type"])
        self.assertEqual("integer", schema["definitions"]["Address"]["properties"]["door_number"]["type"])

        # allow property extension
        self.assertIn("firstName", schema["properties"])
        self.assertIn("occupation", schema["properties"])
        self.assertIn("idNumber", schema["properties"])

        # allow definition extension
        self.assertIn("post_code", schema["definitions"]["Address"]["properties"])
        self.assertIn("employer", schema["definitions"]["Occupation"]["properties"])
        self.assertIn("country", schema["definitions"]["Address"]["properties"])

    def test_overriding_on_required(self):
        pass

    def test_extension_strategy(self):
        test_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "./test_data/extension_2.json")
        schema = load(test_file, ExtensionStrategy())

        # handle conflict
        self.assertEqual("integer", schema["properties"]["age"]["type"])
        self.assertEqual("string", schema["definitions"]["Address"]["properties"]["door_number"]["type"])

        # allow property extension
        self.assertIn("firstName", schema["properties"])
        self.assertIn("occupation", schema["properties"])
        self.assertIn("idNumber", schema["properties"])

        # allow definition extension
        self.assertIn("post_code", schema["definitions"]["Address"]["properties"])
        self.assertIn("employer", schema["definitions"]["Occupation"]["properties"])
        self.assertIn("country", schema["definitions"]["Address"]["properties"])


def test_extension_on_required(self):
        pass

