# bedrock-tools

A small Python library that simplifies [Amazon Bedrock Converse API function calling](https://docs.aws.amazon.com/bedrock/latest/userguide/tool-use.html) (i.e., tool use).

This library reduces the boilerplate code needed to integrate native Python functions with the Amazon Bedrock Converse API, making it easier to create powerful, tool-augmented conversational AI applications.


### Usage Example

```sh
pip install bedrock-tools
```

```python
from bedrock_tools import BedrockTools

# define native functions as tools (using type annotations)

def add_numbers(a: int, b: int) -> int:
    """Add two numbers together."""
    return a + b


def greet(name: str) -> str:
    """Greet a person by name."""
    return f"Hello, {name}!"


def get_weather(city: str, state: str) -> dict:
    """Get the weather for a location."""
    return {
        "city": city,
        "state": state,
        "temperature": "75°F",
        "condition": "Partly Cloudy",
    }

# setup
tools = BedrockTools()
tools.add_function(add_numbers)
tools.add_function(greet)
tools.add_function(get_weather)

# Use the config in your Bedrock Converse API call
response = bedrock.converse(
    modelId=model_id,
    toolConfig=tools.get_tool_config()
    messages=messages,
)

# When you receive a toolUse from the API, invoke the tool
if "toolUse" in content_block:
    tool_results.append(tools.invoke(content_block["toolUse"]))

message = {"role": "user", "content": tool_results}
```


Here's an example (from the [Bedrock Converse API docs](https://docs.aws.amazon.com/bedrock/latest/userguide/tool-use-examples.html)) with and without the library:

![alt text](img/image.png)

![alt text](img/image-2.png)


## Notes

Currently supports function parameters of type:

- scalar
    - str -> string
    - int -> integegr
    - bool -> boolean
    - float -> number
- list
    - str -> string
    - int -> integer
    - bool -> boolean
    - float -> number
- dict -> object


## Development

```
 Choose a make command to run

  init      run this once to initialize a new python project
  install   install project dependencies
  start     run local project
  test      run unit tests
```
