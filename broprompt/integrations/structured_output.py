import json
from dataclasses import dataclass, fields, is_dataclass
from typing import Any, Dict, Type, get_type_hints, get_origin, get_args
import inspect

try:
    from pydantic import BaseModel
    HAS_PYDANTIC = True
except ImportError:
    HAS_PYDANTIC = False
    BaseModel = None


class StructuredOutput:
    """Generate prompts for structured output using Pydantic models or dataclasses"""
    
    def __init__(self, schema_class: Type):
        self.schema_class = schema_class
        self._validate_schema()
    
    def _validate_schema(self):
        """Validate that the schema is either a Pydantic model or dataclass"""
        if HAS_PYDANTIC and issubclass(self.schema_class, BaseModel):
            return
        if is_dataclass(self.schema_class):
            return
        raise ValueError("Schema must be a Pydantic BaseModel or dataclass")
    
    def generate_json_schema(self) -> Dict[str, Any]:
        """Generate JSON schema from the model"""
        if HAS_PYDANTIC and issubclass(self.schema_class, BaseModel):
            return self.schema_class.model_json_schema()
        
        # Handle dataclass
        return self._dataclass_to_json_schema()
    
    def _dataclass_to_json_schema(self) -> Dict[str, Any]:
        """Convert dataclass to JSON schema"""
        schema = {
            "type": "object",
            "properties": {},
            "required": []
        }
        
        type_hints = get_type_hints(self.schema_class)
        
        for field in fields(self.schema_class):
            field_type = type_hints.get(field.name, field.type)
            schema["properties"][field.name] = self._type_to_json_schema(field_type)
            
            if field.default == dataclass.MISSING and field.default_factory == dataclass.MISSING:
                schema["required"].append(field.name)
        
        return schema
    
    def _type_to_json_schema(self, field_type: Type) -> Dict[str, Any]:
        """Convert Python type to JSON schema type"""
        origin = get_origin(field_type)
        
        if field_type == str:
            return {"type": "string"}
        elif field_type == int:
            return {"type": "integer"}
        elif field_type == float:
            return {"type": "number"}
        elif field_type == bool:
            return {"type": "boolean"}
        elif origin == list:
            args = get_args(field_type)
            if args:
                return {"type": "array", "items": self._type_to_json_schema(args[0])}
            return {"type": "array"}
        elif origin == dict:
            return {"type": "object"}
        else:
            return {"type": "string"}  # fallback
    
    def generate_prompt(self, instruction: str = None) -> str:
        """Generate a prompt for structured output"""
        schema = self.generate_json_schema()
        
        base_instruction = instruction or "Please provide your response in the following JSON format:"
        
        return f"""{base_instruction}

```json
{json.dumps(schema, indent=2)}
```

Ensure your response is valid JSON that matches this schema exactly."""
    
    def parse_response(self, response: str) -> Any:
        """Parse JSON response into the schema object"""
        # Extract JSON from response (handle markdown code blocks)
        json_str = response.strip()
        if json_str.startswith("```json"):
            json_str = json_str[7:]
        if json_str.endswith("```"):
            json_str = json_str[:-3]
        json_str = json_str.strip()
        
        data = json.loads(json_str)
        
        if HAS_PYDANTIC and issubclass(self.schema_class, BaseModel):
            return self.schema_class(**data)
        else:
            return self.schema_class(**data)