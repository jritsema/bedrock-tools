import inspect
import logging
from pydantic import create_model
from typing import get_type_hints, Callable, Any


class BedrockTools:
    def __init__(self):
        self.functions = []

    def add_function(self, func: callable):
        """Add a function to be used as a tool."""
        self.functions.append(func)

    def get_tool_config(self) -> dict:
        """Generate the tool configuration for Amazon Bedrock Converse API."""
        return {
            "tools": [
                {"toolSpec": self._generate_tool_spec(func)}
                for func in self.functions
            ],
            "toolChoice": {
                "auto": {}
            },
        }

    def _generate_tool_spec(self, func: callable) -> dict:
        """Generate a tool specification for a given function."""

        func_name = func.__name__
        docstring = inspect.getdoc(func) or ""

        # Get the type hints of the function parameters
        type_hints = get_type_hints(func)

        # Remove the return type hint if present
        type_hints.pop('return', None)

        # Create a Pydantic model dynamically
        model_fields = {name: (typ, ...) for name, typ in type_hints.items()}
        # model = create_model(func_name, __config__={"arbitrary_types_allowed": True}, **model_fields)
        model = create_model(func_name, **model_fields)

        # Generate JSON schema
        schema = model.model_json_schema()

        # todo: consider adding a property description if it helps the model
        # e.g.
        # "param1": {
        #   "type": "string",
        #   "description": "Parameter param1 of type string"
        # },

        return {
            "name": func_name,
            "description": docstring,
            "inputSchema": {
                "json": {
                    "type": schema["type"],
                    "properties": schema["properties"],
                    "required": schema["required"]
                }
            }
        }

    def invoke(self, tool_use: dict) -> any:
        """
        Invokes a tool function based on the tool use request from the converse API
        and returns a content block with the tool result object.
        Exceptions returned from the tool function are caught and
        returned as an error in the content block.

        :param tool_use: The tool use request from the converse API.
        :return: Returns a content block with a tool result object containing
        the result of the tool invocation.
        :raises ValueError: If the tool name is not found in the registered tools.
        """

        tool_use_id = tool_use["toolUseId"]
        tool_name = tool_use["name"]
        tool_input = tool_use["input"]

        for func in self.functions:
            if func.__name__ == tool_name:

                params = {param_name: func.__annotations__.get(param_name, str)(param_value)
                          for param_name, param_value in tool_input.items()}

                logging.info(
                    f"Invoking tool '{tool_name}' with params: {params}")

                try:
                    result = func(**params)

                except Exception as e:
                    logging.error(f"Error invoking tool '{tool_name}': {e}")
                    return {
                        "toolResult": {
                            "toolUseId": tool_use_id,
                            "status": "error",
                            "content": [{"text":  e.args[0]}],
                        }
                    }

                # if result is a scalar value or list,
                # wrap result in a json object to satisfy the converse API
                if isinstance(result, list) or not isinstance(result, dict):
                    result = {"result": result}

                return {
                    "toolResult": {
                        "toolUseId": tool_use_id,
                        "content": [{"json": result}],
                    }
                }

        raise ValueError(f"Tool '{tool_name}' not found")
