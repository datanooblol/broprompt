import re
from typing import Any, Optional, List

class PromptParams:
    """Dynamic parameter container for template variables.
    
    Use this to access and modify template parameters via dot notation.
    Example: params.role = "assistant"
    """
    
    def __init__(self, params: Optional[List[str]]):
        self._params = params or []
        if params:
            for param in params:
                setattr(self, param, None)
    
    def __repr__(self) -> str:
        attrs = ["{}={}".format(k, v) for k, v in self.__dict__.items() if not k.startswith('_')]
        return "PromptParams({})".format(', '.join(attrs))

class Prompt:
    """Main prompt template manager.
    
    Use this class to load markdown templates, manage parameters,
    and generate final prompt strings.
    """
    
    def __init__(self, template: str, params: Optional[List[str]]):
        """Initialize prompt with template and parameter list.
        
        Args:
            template: Raw template string with {param} placeholders
            params: List of parameter names found in template
        """
        self.template: str = template
        self.params: Optional[PromptParams] = PromptParams(params) if params else None
    
    @classmethod
    def from_markdown(cls, file_path: str = "prompt.md"):
        """Load prompt template from markdown file.
        
        Use this method to create a Prompt instance from a .md file.
        The file should contain {parameter_name} placeholders.
        
        Args:
            file_path: Path to markdown file
            
        Returns:
            Prompt instance with loaded template and detected parameters
            
        Raises:
            ValueError: If file doesn't have .md extension
        """
        if not file_path.endswith('.md'):
            raise ValueError("File must be in markdown format (.md extension)")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            template = f.read().strip()
        
        params = re.findall(r'\{([^}]+)\}', template)
        return cls(template, params)
    
    @property
    def str(self) -> str:
        """Generate final prompt string by combining template with parameters.
        
        Use this property to get the complete prompt with all parameter
        values substituted into the template.
        
        Returns:
            Final prompt string with parameters replaced
        """
        if not self.params:
            return self.template
        
        result = self.template
        for param in self.params._params:
            value = getattr(self.params, param, None)
            if value is not None:
                result = result.replace("{{{}}}".format(param), str(value))
        return result
    
    def to_dict(self) -> dict:
        """Export all parameter values to dictionary.
        
        Use this method to save current parameter state or
        pass parameters to other systems.
        
        Returns:
            Dictionary with parameter names as keys and values
        """
        if not self.params:
            return {}
        return {k: v for k, v in self.params.__dict__.items() if not k.startswith('_')}
    
    def from_dict(self, data: dict) -> None:
        """Load parameter values from dictionary.
        
        Use this method to bulk-update parameters from a dictionary.
        Only updates parameters that exist in the template.
        
        Args:
            data: Dictionary with parameter names and values
        """
        if not self.params:
            return
        for key, value in data.items():
            if key in self.params._params:
                setattr(self.params, key, value)