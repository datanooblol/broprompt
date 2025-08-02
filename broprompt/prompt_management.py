import re
from typing import Any, Optional, List

class PromptParams:
    """Dynamic object for accessing template parameters via dot notation"""
    
    def __init__(self, params: Optional[List[str]]):
        self._params = params or []
        if params:
            for param in params:
                setattr(self, param, None)
    
    def __getattr__(self, name: str) -> Any:
        if name in self._params:
            return None
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")
    
    def __setattr__(self, name: str, value: Any) -> None:
        if name.startswith('_'):
            super().__setattr__(name, value)
        else:
            super().__setattr__(name, value)
    
    def __repr__(self) -> str:
        attrs = [f"{k}={v}" for k, v in self.__dict__.items() if not k.startswith('_')]
        return f"PromptParams({', '.join(attrs)})"

class PromptResult:
    """Result object with template and params accessible via dot notation"""
    
    def __init__(self, template: str, params: Optional[List[str]]):
        self.template: str = template
        self.params: Optional[PromptParams] = PromptParams(params) if params else None
    
    @property
    def str(self) -> str:
        """Combine template and params into final prompt string"""
        if not self.params:
            return self.template
        
        result = self.template
        for param in self.params._params:
            value = getattr(self.params, param, None)
            if value is not None:
                result = result.replace(f"{{{param}}}", str(value))
        return result
    
    def to_dict(self) -> dict:
        """Export params to dictionary"""
        if not self.params:
            return {}
        return {k: v for k, v in self.params.__dict__.items() if not k.startswith('_')}
    
    def from_dict(self, data: dict) -> None:
        """Load and update params from dictionary"""
        if not self.params:
            return
        for key, value in data.items():
            if key in self.params._params:
                setattr(self.params, key, value)

def load_markdown_prompt(file_path="prompt.md"):
    """Load prompt from markdown file
    
    Args:
        file_path (str): Path to the markdown prompt file. Defaults to "prompt.md".

    Returns:
        PromptResult: Object with 'template' (str) and 'params' (PromptParams or None)
    
    Raises:
        ValueError: If file is not in markdown format (.md extension)
    """
    if not file_path.endswith('.md'):
        raise ValueError("File must be in markdown format (.md extension)")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        template = f.read().strip()
    
    params = re.findall(r'\{([^}]+)\}', template)
    return PromptResult(template, params)