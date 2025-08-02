# broprompt

Lightweight Python library for prompt template management with dynamic parameter handling.

## Features

- Load prompt templates from markdown files
- Dynamic parameter access via dot notation
- Template + parameter combination into final prompt strings
- Export/import parameters as dictionaries
- Function-to-tool conversion utilities
- Parameter validation and extraction

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
from broprompt.tools import convert_to_tool, register_tools

# Convert function to tool definition
def my_function(name: str, age: int) -> str:
    """Greets a person with their name and age."""
    return f"Hello {name}, you are {age} years old!"

tool_def = convert_to_tool(my_function)

# Register multiple tools
tools = register_tools([my_function])
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
