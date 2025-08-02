import inspect
import json
from typing import Any, Dict, List, Callable, get_type_hints, get_origin, get_args


class ToolDefinition:
    """Tool definition for function calling"""
    
    def __init__(self, name: str, description: str, parameters: Dict[str, Any]):
        self.name = name
        self.description = description
        self.parameters = parameters
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary format"""
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.parameters
            }
        }
    
    def to_openai_format(self) -> Dict[str, Any]:
        """Convert to OpenAI function calling format"""
        return self.to_dict()


class ToolRegistry:
    """Registry for managing tools"""
    
    def __init__(self):
        self.tools: Dict[str, ToolDefinition] = {}
        self.functions: Dict[str, Callable] = {}
    
    def register(self, func: Callable, description: str = None) -> 'ToolRegistry':
        """Register a function as a tool"""
        name = func.__name__
        desc = description or func.__doc__ or f"Function {name}"
        
        # Generate parameter schema
        parameters = self._generate_parameters_schema(func)
        
        tool_def = ToolDefinition(name, desc, parameters)
        self.tools[name] = tool_def
        self.functions[name] = func
        
        return self
    
    def _generate_parameters_schema(self, func: Callable) -> Dict[str, Any]:
        """Generate JSON schema for function parameters"""
        sig = inspect.signature(func)
        type_hints = get_type_hints(func)
        
        schema = {
            "type": "object",
            "properties": {},
            "required": []
        }
        
        for param_name, param in sig.parameters.items():
            if param_name == 'self':
                continue
                
            param_type = type_hints.get(param_name, str)
            param_schema = self._type_to_json_schema(param_type)
            
            # Add description from docstring if available
            if func.__doc__:
                # Simple extraction - could be enhanced
                param_schema["description"] = f"Parameter {param_name}"
            
            schema["properties"][param_name] = param_schema
            
            # Check if parameter is required
            if param.default == inspect.Parameter.empty:
                schema["required"].append(param_name)
        
        return schema
    
    def _type_to_json_schema(self, param_type: Any) -> Dict[str, Any]:
        """Convert Python type to JSON schema"""
        origin = get_origin(param_type)
        
        if param_type == str:
            return {"type": "string"}
        elif param_type == int:
            return {"type": "integer"}
        elif param_type == float:
            return {"type": "number"}
        elif param_type == bool:
            return {"type": "boolean"}
        elif origin == list:
            args = get_args(param_type)
            if args:
                return {"type": "array", "items": self._type_to_json_schema(args[0])}
            return {"type": "array"}
        elif origin == dict:
            return {"type": "object"}
        else:
            return {"type": "string"}
    
    def get_tool_definitions(self) -> List[Dict[str, Any]]:
        """Get all tool definitions in API format"""
        return [tool.to_dict() for tool in self.tools.values()]
    
    def call_tool(self, name: str, arguments: Dict[str, Any]) -> Any:
        """Execute a registered tool"""
        if name not in self.functions:
            raise ValueError(f"Tool {name} not found")
        
        func = self.functions[name]
        return func(**arguments)
    
    def generate_tool_prompt(self) -> str:
        """Generate prompt describing available tools"""
        if not self.tools:
            return "No tools available."
        
        parts = ["Available tools:"]
        
        for tool in self.tools.values():
            parts.append(f"\n{tool.name}: {tool.description}")
            
            # Add parameter info
            if tool.parameters.get("properties"):
                params = []
                required = tool.parameters.get("required", [])
                
                for param_name, param_info in tool.parameters["properties"].items():
                    param_str = f"{param_name} ({param_info['type']})"
                    if param_name in required:
                        param_str += " [required]"
                    params.append(param_str)
                
                if params:
                    parts.append(f"  Parameters: {', '.join(params)}")
        
        return "\n".join(parts)


def tool(description: str = None):
    """Decorator to register a function as a tool"""
    def decorator(func: Callable) -> Callable:
        func._tool_description = description
        return func
    return decorator