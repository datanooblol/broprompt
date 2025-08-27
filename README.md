# broprompt

Lightweight Python library for prompt template management with dynamic parameter handling.

## Features

- Load prompt templates from markdown files
- Dynamic parameter access via dot notation
- Template + parameter combination into final prompt strings
- Export/import parameters as dictionaries
- Function-to-tool conversion utilities
- Parameter validation and extraction
- Examples repository with prompt techniques and integration patterns

## Usage

```python
from broprompt.prompt_engineering import Prompt

# Load template from markdown file
prompts = Prompt.from_markdown("system_prompt.md")

# Set parameters
prompts.params.role = "assistant"
prompts.params.domain = "coding"

# Get final prompt string
final_prompt = prompts.str

# Export parameters
params_dict = prompts.to_dict()

# Import parameters
prompts.from_dict({"role": "expert", "tone": "professional"})
```

### Tools Module

```python
from broprompt import Prompt, list_tools, parse_codeblock_to_dict, get_yaml_function_definition, validate_parameters

# Define functions with <|start|><|end|> tokens for descriptions
def save_file(filename: str, content: str):
    """
    <|start|>This will be used only when a user ask for saving something<|end|>
    Args:
        filename (str): The name of the file to save.
        content (str): The content to write into the file.
    """
    return f"File {filename} saved with content length {len(content)}"

def add_calendar(date: str, time: str, description: str):
    """
    <|start|>This will be used only when a user ask for adding something to their calendar<|end|>
    Args:
        date (str): The date to add to the calendar in YYYY-MM-DD format.
        time (str): The time to add to the calendar in HH:MM format.
        description (str): A brief description of the event.
    """
    return f"Event '{description}' added to calendar on {date} at {time}"

tools = [save_file, add_calendar]

# Load tool selector prompt and populate with tools
tool_selector_prompt = Prompt.from_markdown("./tool_selector.md")
tool_selector_prompt.from_dict({"tools": list_tools(tools)})

# Select tool based on user message
message = "I have to visit my aunt on 2024-10-01 at 15:00. Add it to my calendar"
tool_response = model.run(system_prompt=tool_selector_prompt.str, messages=[model.UserMessage(message)])
tool = parse_codeblock_to_dict(tool_response, codeblock="yaml")

# Get selected tool and its YAML definition
selected_tool = [t for t in tools if t.__name__ == tool.get("tool", "nope")][0]
tool_definition = get_yaml_function_definition(selected_tool)

# Extract parameters using tool call prompt
tool_call_prompt = Prompt.from_markdown("./tool_call.md")
tool_call_prompt.from_dict({"definition": tool_definition})
params_response = model.run(tool_call_prompt.str, [model.UserMessage(message)])
params = parse_codeblock_to_dict(params_response, codeblock="yaml")

# Validate and execute
is_valid, error = validate_parameters(params, selected_tool)
if is_valid:
    result = selected_tool(**params)
```

### Structured Output

```python
from broprompt import Prompt, parse_codeblock_to_dict, get_yaml_schema_definition
from pydantic import BaseModel, Field
from typing import Literal

# Define Pydantic models
class User(BaseModel):
    """This is a user model that contains name and age."""
    name: str = Field(..., description="the name of the user")
    age: int = Field(..., description="the age of the user")

class Sentiment(BaseModel):
    """This is a sentiment model that extract sentiment from INPUT with its explanation."""
    sentiment: Literal["positive", "neutral", "negative"] = Field(..., description="read INPUT and classify the sentiment")
    evidence: str = Field(..., description="provide evidence from INPUT to support the sentiment")
    explanation: str = Field(..., description="what is the reason for the sentiment")

# Generate YAML schema definitions
user_schema = get_yaml_schema_definition(User, as_array=True)  # For multiple users
sentiment_schema = get_yaml_schema_definition(Sentiment, as_array=False)  # For single sentiment

# Load structured output prompt template
so_prompt = Prompt.from_markdown("./structured_output.md")
so_prompt.from_dict({"definition": user_schema})

# Extract structured data
response = model.run(system_prompt=so_prompt.str, messages=[model.UserMessage("Jake is 30 years old, but Kate is 5 year younger than him.")])
users_data = parse_codeblock_to_dict(response)
users = [User(**item) for item in users_data]
```

### Context Module

```python
from broprompt.context import Context

# Create a context (LangChain Document equivalent)
ctx = Context(
    context="This is the document content",
    metadata={"source": "file.txt", "type": "text"}
)

# Access content
print(ctx.context)  # Direct access

# Automatic fields
print(ctx.id)         # Auto-generated UUID
print(ctx.created_at) # UTC timestamp
```

## Template Format

Use `{parameter_name}` placeholders in your markdown files:

```markdown
# System Prompt

You are {role}, specialized in {domain}.
Respond in {tone} tone.
```
