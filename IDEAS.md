# broprompt - Ideas & Architecture

## Vision
Lightweight library for prompt and context manipulation supporting structured output, tool calling, and various prompt engineering patterns like ReACT, Reflection, etc. Supports zero-shot, one-shot, and few-shot learning.

## Core Architecture

### Module Structure
```
broprompt/
├── core/
│   ├── templates.py      # Template management & formatting
│   ├── examples.py       # Few-shot learning support
│   └── context.py        # Context manipulation
├── patterns/
│   ├── react.py          # ReACT pattern
│   ├── reflection.py     # Reflection pattern
│   └── chain_of_thought.py
├── integrations/
│   ├── structured_output.py  # Pydantic/Dataclass schema
│   └── tool_calling.py       # Function calling support
└── utils/
    └── validators.py     # Input validation
```

## Key Features

### 1. Template Engine
- Extend current `load_system_prompt` with advanced formatting
- Support for Jinja2-like features
- Variable substitution and conditional logic

### 2. Example Management (Few-shot Learning)
- Easy example injection for few-shot prompts
- Example formatting and organization
- Dynamic example selection based on context

### 3. Pattern Builders
- Fluent API for common patterns
- ReACT: Thought → Action → Observation cycles
- Reflection: Initial response → Critique → Refined response
- Chain of Thought: Step-by-step reasoning

### 4. Context Management
- Smart context window handling
- Token limit awareness
- Context compression and prioritization

### 5. Structured Output
- Integration with Pydantic models and dataclasses
- JSON schema generation
- Type validation and conversion

### 6. Tool Calling Support
- Function schema generation
- Tool definition management
- Integration with LLM function calling APIs

## API Design Philosophy

### Simple Usage
```python
prompt = Prompt.system("system_prompt.md").user("What is {topic}?")
```

### Pattern Usage
```python
react_prompt = ReACT().thought().action().observation().build()
```

### Few-shot Learning
```python
few_shot = FewShot().add_example(input="...", output="...").build()
```

### Structured Output
```python
@dataclass
class Response:
    answer: str
    confidence: float

structured = StructuredOutput(Response).generate_prompt()
```

## Implementation Priorities
1. Core template engine improvements
2. Structured output integration
3. Pattern builders (ReACT, Reflection)
4. Few-shot learning support
5. Tool calling integration
6. Context management utilities