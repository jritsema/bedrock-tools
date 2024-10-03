import unittest
from bedrock_tools import BedrockTools
import json


class TestBedrockTools(unittest.TestCase):

    def setUp(self):
        self.generator = BedrockTools()

    def test_docstring_handling(self):

        def func_with_docstring(x: int):
            """This is a test function."""
            pass

        def func_without_docstring(y: str):
            pass

        spec1 = self.generator._generate_tool_spec(func_with_docstring)
        spec2 = self.generator._generate_tool_spec(func_without_docstring)

        self.assertEqual(spec1["description"], "This is a test function.")
        self.assertEqual(spec2["description"], "")

    def test_generate_tool_spec_scalar(self):

        def sample_function(param1: str, param2: int, param3: bool, param4: float = 0.0):
            """Sample function docstring."""
            pass

        spec = self.generator._generate_tool_spec(sample_function)
        print(json.dumps(spec, indent=2))

        self.assertEqual(spec["name"], "sample_function")
        self.assertEqual(spec["description"], "Sample function docstring.")
        self.assertEqual(spec["inputSchema"]["json"]["type"], "object")
        self.assertEqual(len(spec["inputSchema"]["json"]["properties"]), 4)

        properties = spec["inputSchema"]["json"]["properties"]
        for prop in properties:
            p = properties[prop]
            if prop == "param1":
                self.assertEqual(p["type"], "string")
            if prop == "param2":
                self.assertEqual(p["type"], "integer")
            if prop == "param3":
                self.assertEqual(p["type"], "boolean")
            if prop == "param4":
                self.assertEqual(p["type"], "number")

        self.assertEqual(spec["inputSchema"]["json"]
                         ["required"], ["param1", "param2", "param3", "param4"])

    def test_generate_tool_spec_list_string(self):

        def complex_func(this_is_a_list_of_strings: list[str]):
            """list of strings"""
            pass

        spec = self.generator._generate_tool_spec(complex_func)
        print(json.dumps(spec, indent=2))

        prop = spec["inputSchema"]["json"]["properties"]["this_is_a_list_of_strings"]
        self.assertEqual(prop["type"], "array")
        self.assertEqual(prop["items"]["type"], "string")

    def test_generate_tool_spec_list_int(self):

        def complex_func(this_is_a_list_of_integers: list[int]):
            """list of ints"""
            pass

        spec = self.generator._generate_tool_spec(complex_func)
        print(json.dumps(spec, indent=2))

        prop = spec["inputSchema"]["json"]["properties"]["this_is_a_list_of_integers"]
        self.assertEqual(prop["type"], "array")
        self.assertEqual(prop["items"]["type"], "integer")

    def test_generate_tool_spec_dict(self):

        def complex_func(this_is_a_dictionary: dict):
            """dictionary"""
            pass

        spec = self.generator._generate_tool_spec(complex_func)
        print(json.dumps(spec, indent=2))

        prop = spec["inputSchema"]["json"]["properties"]["this_is_a_dictionary"]
        self.assertEqual(prop["type"], "object")

    def test_get_tool_config(self):

        def func1(a: str):
            pass

        def func2(b: int, c: float):
            pass

        self.generator.add_function(func1)
        self.generator.add_function(func2)

        config = self.generator.get_tool_config()

        self.assertEqual(len(config["tools"]), 2)
        self.assertEqual(config["tools"][0]["toolSpec"]["name"], "func1")
        self.assertEqual(config["tools"][1]["toolSpec"]["name"], "func2")


if __name__ == '__main__':
    unittest.main()
