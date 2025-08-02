# broprompt

Lightweight Python library for prompt template management with dynamic parameter handling.

## Features

- Load prompt templates from markdown files
- Dynamic parameter access via dot notation
- Template + parameter combination into final prompt strings
- Export/import parameters as dictionaries

## Usage

```python
from broprompt.prompt_management import load_markdown_prompt

# Load template from markdown file
prompts = load_markdown_prompt("system_prompt.md")

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

## Template Format

Use `{parameter_name}` placeholders in your markdown files:

```markdown
# System Prompt

You are {role}, specialized in {domain}.
Respond in {tone} tone.
```
