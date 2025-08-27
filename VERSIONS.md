# Version History

## 0.1.5 (YAML Function & Schema Definition)
- Enhanced `get_yaml_function_definition()` to generate cleaner YAML schema templates
- Added `get_yaml_schema_definition()` for Pydantic model to YAML schema conversion
- Support for structured output extraction with array and single object formats
- Improved string parameter formatting with proper quotes in YAML output
- Streamlined function definition prompts for better LLM integration
- Added examples repository with prompt techniques and integration patterns

## 0.1.4 (Context Registration)
- Registered Context class in __init__.py for direct import access

## 0.1.3 (Context Module)
- Added `broprompt.context` module with Context dataclass equivalent to LangChain Document
- Context includes `context`, `metadata`, auto-generated `id`, and UTC `created_at` timestamp

## 0.1.2 (Tools Module)
- Added `broprompt.tools` module for function-to-tool conversion
- Function signature analysis and JSON schema generation
- Tool registration and parameter validation utilities
- YAML/JSON parameter extraction from user input

## 0.1.1 (API Update)
- Updated to use `Prompt.from_markdown()` method instead of `load_markdown_prompt()` function
- Corrected import path to `broprompt.prompt_engineering`

## 0.1.0 (Initial Release)
- Added `load_markdown_prompt()` function
- Dynamic parameter access via dot notation
- Template string combination with `.str` property
- Parameter export/import with `to_dict()` and `from_dict()` methods